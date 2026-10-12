import importlib

import traceback



from flask import Flask, jsonify, render_template, request



from config import get_org_config_status

from lab_context import inject_answers

from lab_store import answers_for_variables, clear_variables, merge_answers

from lab_ui import enrich_step, get_part_variables

from lab_verify import verify_step_answers

from lab_api_cache import cached as cache_get, invalidate, invalidate_prefix

from progress import get_all_progress, get_module_progress, get_step_access, is_setup_complete, is_step_unlocked



app = Flask(__name__)



MODULE_IMPORTS = [

    "modules.module0_setup",

    "modules.module1_users",

    "modules.module2_org_data",

    "modules.module3_graphql",

    "modules.module4_webex_apis",

    "modules.module5_dashboard",

]





def get_modules():

    """Load lab modules and inject saved dashboard answers."""

    modules = []

    for name in MODULE_IMPORTS:

        mod = importlib.import_module(name)

        inject_answers(mod)

        modules.append(mod)

    return modules





def get_module_by_id(module_id: str):

    return next((m for m in get_modules() if m.MODULE_ID == module_id), None)


def _refresh_requested() -> bool:

    return str(request.args.get("refresh", "")).lower() in ("1", "true", "yes")


def json_cached(cache_key, loader, ttl=300):

    try:

        return jsonify(cache_get(cache_key, loader, force=_refresh_requested(), ttl=ttl))

    except Exception as e:

        return jsonify({"error": str(e)}), 500





def build_workspace(modules) -> dict:

    stored = answers_for_variables(

        [var for mod in modules for step in mod.STEPS for var in step.get("variables", [])]

    )

    module_payload = []

    for mod in modules:

        module_id = mod.MODULE_ID

        progress = get_module_progress(mod, modules)

        module_payload.append(

            {

                "module_id": module_id,

                "module_name": mod.MODULE_NAME,

                "view_only": getattr(mod, "VIEW_ONLY", False),

                "steps": [

                    {**enrich_step(module_id, step, stored), "access": get_step_access(mod, step, modules)}

                    for step in mod.STEPS

                ],

                "completed_steps": progress["completed_steps"],

                "total_steps": progress["total_steps"],

            }

        )

    return {"modules": module_payload, "setup_complete": is_setup_complete(modules)}





@app.route("/")

def dashboard():

    modules = get_modules()

    progress = get_all_progress(modules)

    config_status = get_org_config_status()
    from lab_setup import oauth_setup_payload

    return render_template(
        "dashboard.html",
        progress=progress,
        token_configured=config_status["token_configured"],
        org_configured=config_status["org_configured"],
        org_id_mismatch=config_status["org_id_mismatch"],
        org_id=config_status["org_id"],
        token_org_id=config_status["token_org_id"],
        setup_complete=progress.get("setup_complete", False),
        credential_source=config_status.get("credential_source", "none"),
        auth_method=config_status.get("auth_method", ""),
        setup_oauth=oauth_setup_payload(request.host_url),
    )





@app.route("/dashboard")
def full_dashboard():
    """Stand-alone Full Dashboard page (no lab module chrome)."""
    modules = get_modules()
    progress = get_all_progress(modules)
    config_status = get_org_config_status()
    return render_template(
        "full_dashboard.html",
        progress=progress,
        token_configured=config_status["token_configured"],
        org_configured=config_status["org_configured"],
        org_id_mismatch=config_status["org_id_mismatch"],
        org_id=config_status["org_id"],
        token_org_id=config_status["token_org_id"],
        setup_complete=progress.get("setup_complete", False),
        credential_source=config_status.get("credential_source", "none"),
    )


@app.route("/setup/callback")
def setup_oauth_callback():
    """OAuth redirect target. Shows the authorization code so it can be pasted into Setup."""
    return render_template(
        "setup_callback.html",
        code=request.args.get("code") or "",
        error=request.args.get("error") or "",
        error_description=request.args.get("error_description") or "",
    )


@app.route("/api/lab/setup/oauth")
def api_setup_oauth():
    from lab_setup import oauth_setup_payload

    return jsonify(oauth_setup_payload(request.host_url))


@app.route("/api/lab/setup/integration", methods=["POST"])
def api_setup_integration():
    from lab_setup import exchange_integration_code, setup_callback_url

    payload = request.get_json(silent=True) or {}
    result = exchange_integration_code(
        payload.get("client_id") or "",
        payload.get("client_secret") or "",
        payload.get("code") or "",
        setup_callback_url(request.host_url),
    )
    if not result.get("valid"):
        return jsonify(
            {
                "valid": False,
                "message": result.get("message")
                or "Could not generate an access token. Fix the highlighted fields using the hints below.",
                "errors": result.get("errors") or [],
                "missing_scopes": result.get("missing_scopes") or [],
            }
        ), 422

    merge_answers(result.get("normalized") or {"SETUP_BEARER_TOKEN": "__saved__"})
    invalidate_prefix("")

    modules = get_modules()
    module = get_module_by_id("module0")
    stored = answers_for_variables(
        [var for step in module.STEPS for var in step.get("variables", [])] if module else []
    )
    return jsonify(
        {
            "valid": True,
            "progress": get_all_progress(modules),
            "config_status": get_org_config_status(),
            "step": enrich_step(module.MODULE_ID, module.STEPS[0], stored) if module else None,
            "org_id": result.get("org_id") or "",
        }
    )


@app.route("/api/config/status")

def api_config_status():

    """Return active org/token configuration (no secrets). Useful after editing .env."""

    return jsonify(get_org_config_status())





@app.route("/api/progress")

def api_progress():

    modules = get_modules()

    return jsonify(get_all_progress(modules))





@app.route("/api/lab/workspace")

def api_lab_workspace():

    modules = get_modules()

    return jsonify(build_workspace(modules))





@app.route("/api/lab/steps/<module_id>/<step_id>", methods=["PUT"])

def api_save_step(module_id, step_id):

    modules = get_modules()

    module_map = {m.MODULE_ID: m for m in modules}

    module = module_map.get(module_id)

    if not module:

        return jsonify({"error": "Module not found"}), 404



    step = next((s for s in module.STEPS if s["id"] == step_id), None)

    if not step:

        return jsonify({"error": "Step not found"}), 404



    payload = request.get_json(silent=True) or {}

    raw_answers = payload.get("answers")

    if not isinstance(raw_answers, dict):

        return jsonify({"error": "Expected JSON body with an answers object"}), 400



    allowed = set(step.get("variables", []))

    part_id = payload.get("part")

    if part_id:

        part_vars = get_part_variables(module_id, step_id, part_id)

        if not part_vars:

            return jsonify({"error": "Unknown step part"}), 400

        verify_vars = part_vars

        updates = {k: v for k, v in raw_answers.items() if k in part_vars}

    else:

        verify_vars = step.get("variables", [])

        updates = {k: v for k, v in raw_answers.items() if k in allowed}

    if not updates:

        return jsonify({"error": "No valid answer fields provided"}), 400



    if not is_step_unlocked(module, step_id, modules):

        return jsonify({"error": "Complete earlier steps in this module before saving this step."}), 403



    if module_id == "module0":

        from lab_setup import verify_setup_step



        verification = verify_setup_step(step_id, updates)

        if not verification["valid"]:

            return jsonify(

                {

                    "valid": False,

                    "message": verification.get("message")

                    or "Could not save credentials. Fix the highlighted fields using the hints below.",

                    "errors": verification["errors"],

                }

            ), 422

    else:

        if not is_setup_complete(modules):

            return jsonify({"error": "Complete the Setup module before saving lab answers."}), 403



        verification = verify_step_answers(module_id, step_id, verify_vars, updates)

        if not verification["valid"]:

            return jsonify(

                {

                    "valid": False,

                    "message": "Some answers are incorrect. Fix the highlighted fields using the hints below.",

                    "errors": verification["errors"],

                }

            ), 422



        merge_answers(verification.get("normalized") or updates)
        invalidate_prefix("")



    modules = get_modules()

    module = next(m for m in modules if m.MODULE_ID == module_id)

    stored = answers_for_variables(step.get("variables", []))

    progress = get_all_progress(modules)

    config_status = get_org_config_status()

    return jsonify(

        {

            "valid": True,

            "step": enrich_step(module_id, step, stored),

            "progress": progress,

            "config_status": config_status,

        }

    )





@app.route("/api/lab/modules/<module_id>/reset", methods=["POST"])

def api_reset_module(module_id):

    modules = get_modules()

    module = next((m for m in modules if m.MODULE_ID == module_id), None)

    if not module:

        return jsonify({"error": "Module not found"}), 404



    variables: list[str] = []

    for step in module.STEPS:

        variables.extend(step.get("variables", []))



    if module_id == "module0":

        from lab_credentials import clear_credentials



        clear_credentials()

        clear_variables(variables)
        invalidate_prefix("")

    else:

        clear_variables(variables)
        invalidate_prefix("")



    modules = get_modules()

    module = next(m for m in modules if m.MODULE_ID == module_id)

    stored = answers_for_variables(

        [var for step in module.STEPS for var in step.get("variables", [])]

    )

    progress = get_all_progress(modules)

    return jsonify(

        {

            "module_id": module_id,

            "progress": progress,

            "config_status": get_org_config_status(),

            "steps": [

                {**enrich_step(module_id, step, stored), "access": get_step_access(module, step, modules)}

                for step in module.STEPS

            ],

        }

    )





@app.route("/api/module/<module_id>/progress")

def api_module_progress(module_id):

    modules = get_modules()

    module_map = {m.MODULE_ID: m for m in modules}

    module = module_map.get(module_id)

    if not module:

        return jsonify({"error": "Module not found"}), 404

    return jsonify(get_module_progress(module, modules))





# --- Module 1: Users ---

@app.route("/api/users")

def api_users():

    def load():

        module1 = get_module_by_id("module1")

        return {"users": module1.fetch_users()}

    return json_cached("users", load)





# --- Module 2: Org Data ---

@app.route("/api/org/entry-points")

def api_entry_points():

    def load():

        module2 = get_module_by_id("module2")

        return {"entry_points": module2.fetch_entry_points()}

    return json_cached("org:entry_points", load)





@app.route("/api/org/queues")

def api_queues():

    def load():

        module2 = get_module_by_id("module2")

        return {"queues": module2.fetch_queues()}

    return json_cached("org:queues", load)





@app.route("/api/org/global-variables")

def api_global_variables():

    def load():

        module2 = get_module_by_id("module2")

        return {"global_variables": module2.fetch_global_variables()}

    return json_cached("org:global_variables", load)





@app.route("/api/org/global-variables/<variable_id>", methods=["GET"])
def api_get_global_variable(variable_id):
    try:
        module2 = get_module_by_id("module2")
        return jsonify(module2.get_global_variable_edit_form(variable_id))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/org/global-variables/<variable_id>", methods=["PUT"])
def api_update_global_variable(variable_id):
    try:
        module2 = get_module_by_id("module2")
        payload = request.get_json(silent=True) or {}
        if not isinstance(payload, dict):
            return jsonify({"error": "Expected a JSON object"}), 400
        if "value" in payload and "defaultValue" not in payload:
            payload["defaultValue"] = payload.get("value")
        updated = module2.update_global_variable(variable_id, payload)
        invalidate("org:global_variables")
        return jsonify({"global_variable": updated})
    except Exception as e:
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500





@app.route("/api/org/aux-codes")

def api_aux_codes():

    def load():

        module2 = get_module_by_id("module2")

        return {"aux_codes": module2.fetch_aux_codes()}

    return json_cached("org:aux_codes", load)





@app.route("/api/org/teams")

def api_teams():

    def load():

        module2 = get_module_by_id("module2")

        return {"teams": module2.fetch_teams()}

    return json_cached("org:teams", load)





# --- Module 3: GraphQL Reports ---

@app.route("/api/reports/csr")

def api_csr():

    def load():

        module3 = get_module_by_id("module3")

        return {"records": module3.fetch_csr_report()}

    return json_cached("reports:csr", load)





@app.route("/api/reports/car")

def api_car():

    try:

        module3 = get_module_by_id("module3")

        return jsonify({"records": module3.fetch_car_report()})

    except Exception as e:

        return jsonify({"error": str(e)}), 500





@app.route("/api/reports/asr")

def api_asr():

    def load():

        module3 = get_module_by_id("module3")

        return {"records": module3.fetch_asr_report()}

    return json_cached("reports:asr", load)





@app.route("/api/reports/aar")

def api_aar():

    try:

        module3 = get_module_by_id("module3")

        return jsonify({"records": module3.fetch_aar_report()})

    except Exception as e:

        return jsonify({"error": str(e)}), 500





@app.route("/api/reports/csr-details")

def api_csr_details():

    try:

        module3 = get_module_by_id("module3")

        return jsonify({"records": module3.fetch_csr_details()})

    except Exception as e:

        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500





@app.route("/api/reports/car/<task_id>")

def api_car_for_task(task_id):

    try:

        module3 = get_module_by_id("module3")

        car = module3.fetch_car_for_task(task_id)

        return jsonify({"records": car["records"], "entry_point": car["entry_point"], "task_id": task_id})

    except Exception as e:

        return jsonify({"error": str(e)}), 500





@app.route("/api/reports/asr-details")

def api_asr_details():

    try:

        module3 = get_module_by_id("module3")

        return jsonify({"records": module3.fetch_asr_details()})

    except Exception as e:

        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500





@app.route("/api/reports/aar/<agent_session_id>")

def api_aar_for_session(agent_session_id):

    try:

        module3 = get_module_by_id("module3")

        return jsonify({"records": module3.fetch_aar_for_session(agent_session_id), "agent_session_id": agent_session_id})

    except Exception as e:

        return jsonify({"error": str(e)}), 500





@app.route("/api/reports/query/<report_id>")

def api_report_query(report_id):

    try:

        module3 = get_module_by_id("module3")

        return jsonify(

            module3.get_report_query(

                report_id,

                task_id=request.args.get("task_id"),

                session_id=request.args.get("session_id"),

            )

        )

    except ValueError as e:

        return jsonify({"error": str(e)}), 404

    except Exception as e:

        return jsonify({"error": str(e)}), 500





@app.route("/api/reports/rt-agents")

def api_rt_agents():

    try:

        module3 = get_module_by_id("module3")

        return jsonify({"agents": module3.fetch_rt_agents()})

    except Exception as e:

        return jsonify({"error": str(e)}), 500





# --- Module 4: Webex APIs ---

@app.route("/api/webex/people")

def api_webex_people():

    def load():

        module4 = get_module_by_id("module4")

        return {"people": module4.fetch_webex_people()}

    return json_cached("webex:people", load)





@app.route("/api/webex/locations")

def api_locations():

    def load():

        module4 = get_module_by_id("module4")

        return {"locations": module4.fetch_locations()}

    return json_cached("webex:locations", load)





@app.route("/api/webex/pstn/<location_id>")

def api_pstn(location_id):

    if _refresh_requested():

        invalidate(f"webex:pstn:{location_id}")

    def load():

        module4 = get_module_by_id("module4")

        return {"pstn": module4.fetch_pstn_connection(location_id)}

    return json_cached(f"webex:pstn_api:{location_id}", load)




@app.route("/api/webex/ep-pstn")

def api_ep_pstn():

    if _refresh_requested():

        invalidate_prefix("webex:pstn")

        invalidate_prefix("webex:pstn_api")

    def load():

        module4 = get_module_by_id("module4")

        return {"numbers": module4.fetch_ep_pstn_numbers()}

    return json_cached("webex:ep_pstn", load)





@app.route("/api/dashboard/info/<section_id>")

def api_dashboard_info(section_id):

    try:

        from lab_dashboard_info import get_section_info

        info = get_section_info(section_id)

        report_query_id = {
            "csr": "csr",
            "csr-details": "csr-details",
            "car": "car",
            "car-events": "car-events",
            "asr": "asr",
            "asr-details": "asr-details",
            "aar": "aar",
            "aar-events": "aar-events",
            "rt-agents": "rt",
        }.get(section_id)

        if report_query_id:

            try:

                module3 = get_module_by_id("module3")

                info["query"] = module3.get_report_query(report_query_id)

            except Exception:

                pass

        return jsonify(info)

    except ValueError as e:

        return jsonify({"error": str(e)}), 404

    except Exception as e:

        return jsonify({"error": str(e)}), 500





if __name__ == "__main__":

    app.run(host="127.0.0.1", port=5000, debug=True)



import os
import glob
import ast

def process_routes():
    res = []
    files = glob.glob('app/routes/*.py') + ['app/auth.py']
    for f in files:
        if not os.path.exists(f): continue
        code = open(f).read()
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    route_path = ""
                    methods = "GET"
                    login_req = False
                    roles = "All"
                    for dec in node.decorator_list:
                        if isinstance(dec, ast.Call) and getattr(dec.func, 'attr', '') == 'route':
                            if dec.args:
                                route_path = dec.args[0].value
                            for kw in dec.keywords:
                                if kw.arg == 'methods':
                                    methods = ",".join([el.value for el in kw.value.elts])
                        elif isinstance(dec, ast.Name) and dec.id == 'login_required':
                            login_req = True
                    if route_path:
                        body_code = ast.unparse(node)
                        if "current_user.role != 'client'" in body_code:
                            roles = "client"
                        elif "require_architect" in body_code or "current_user.role == 'architect'" in body_code:
                            roles = "architect"
                            
                        ret = "unknown"
                        needs_change = "yes"
                        if "render_template" in body_code: 
                            ret = "template render"
                        elif "redirect(" in body_code: 
                            ret = "redirect"
                        elif "jsonify(" in body_code: 
                            ret = "JSON"
                            needs_change = "no (already JSON)"
                            
                        desc = f"Handles {route_path}"
                        params = "none"
                        body = "none"
                        if methods != "GET":
                            body = "multipart/form-data or application/x-www-form-urlencoded depending on form"
                            if "request.get_json" in body_code or "request.is_json" in body_code:
                                body = "JSON payload"
                                
                        block = f"""───────────────────────────────────────────
ENDPOINT: {methods} {route_path}
AUTH: {'login_required' if login_req else 'public'} | roles: {roles}
DESCRIPTION: {desc}
QUERY PARAMS: {params}
REQUEST BODY: {body}
SUCCESS RESPONSE (200):
  {{
    // Depends on implementation. Currently returns {ret}.
  }}
ERROR RESPONSES:
  401 — not authenticated
  403 — wrong role
  404 — resource not found
CURRENTLY RETURNS: {ret}
NEEDS CHANGE FOR API USE: {needs_change} - Replace with jsonify()
───────────────────────────────────────────"""
                        res.append(block)
        except:
            pass
    return "\n\n".join(res)

def get_templates():
    res = []
    for root, _, files in os.walk('app/templates'):
        for file in files:
            if file.endswith('.html'):
                path = os.path.join(root, file)
                rel_path = os.path.relpath(path, 'app/templates')
                content = open(path).read()
                
                react_comp = "yes" if "extends" not in content else "no (layout wrapper)"
                
                block = f"""- Template name: `{rel_path}`
- Page it represents: {os.path.basename(file).replace('.html', '').replace('_', ' ').title()}
- Can it be a single React component? {react_comp}
- Data it needs on load: Context variables passed by Flask (see Pass 1C)
- User interactions: Form submits and JS fetch calls
- Role-specific sections: {'Yes' if 'current_user.role' in content else 'No'}
"""
                res.append(block)
    return "\n".join(res)

with open('docs/API_CONTRACT.md', 'w') as out:
    out.write("# PASS 7A — API CONTRACT DOCUMENT\n\n")
    out.write(process_routes())
    
with open('docs/FRONTEND_REPLACEMENT.md', 'w') as out:
    out.write("# PASS 7B — FRONTEND REPLACEMENT GUIDE\n\n")
    out.write("FRONTEND REPLACEMENT CHECKLIST:\n\n")
    out.write("1. Routes that ALREADY return JSON: `/api/rag/query`, `/api/debug-clients`, `/projects/<id>/update-status-api`\n")
    out.write("2. Routes that return templates but NEED to return JSON for new frontend: All other `GET` routes. Need to map `render_template(..., data=data)` to `return jsonify(data)`.\n")
    out.write("3. Routes that handle file uploads: `/projects/<id>/plot/upload`, `/projects/<id>/documents/upload`, `/projects/<id>/images/upload`, `/projects/<id>/payments/add`. Content-Type must be `multipart/form-data`.\n")
    out.write("4. Routes that use Flask-Login session auth: New frontend needs to handle session cookies (`credentials: 'include'` in fetch).\n")
    out.write("5. Static assets (CSS, fonts, images) currently served from: `/static/`. New frontend should host these independently.\n")
    out.write("6. Environment variables the frontend needs to know: `API_BASE_URL` (e.g. `http://localhost:5002` during dev).\n\n")
    out.write("---\n\n# PASS 7C — TEMPLATE INVENTORY SUMMARY\n\n")
    out.write(get_templates())

import ast
import os
import glob
import re

def get_routes():
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
                        # Check roles
                        body_code = ast.unparse(node)
                        if "current_user.role != 'client'" in body_code:
                            roles = "client"
                        elif "require_architect" in body_code or "current_user.role == 'architect'" in body_code:
                            roles = "architect"
                            
                        ret = "unknown"
                        if "render_template" in body_code: ret = "template"
                        elif "redirect(" in body_code: ret = "redirect"
                        elif "jsonify(" in body_code: ret = "JSON"
                        
                        res.append(f"| {os.path.basename(f)} | `{route_path}` | {methods} | `{node.name}` | {login_req} | {roles} | {ret} |")
        except:
            pass
    return res

with open('docs/ROUTE_INVENTORY.md', 'w') as out:
    out.write("## ═══ PASS 1 — COMPLETE FILE & ROUTE INVENTORY ═══\n\n### TABLE 1A — ALL FLASK ROUTES\n")
    out.write("| File | Decorator | HTTP Methods | Function Name | login_required? | Roles Allowed | Returns |\n")
    out.write("|---|---|---|---|---|---|---|\n")
    for r in get_routes():
        out.write(r + "\n")

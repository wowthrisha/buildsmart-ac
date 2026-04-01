import os, glob, re

def find_routes():
    files = glob.glob('app/routes/*.py') + ['app/auth.py']
    for f in files:
        if not os.path.exists(f): continue
        content = open(f).read()
        routes = re.findall(r'@(?:bp|app)\.route\((.*?)\)(.*?)(?:def (.*?)\():', content, re.DOTALL)
        for r in routes:
            path = r[0].strip('\'"')
            methods = re.search(r'methods=\[(.*?)\]', path)
            methods_str = methods.group(1) if methods else "'GET'"
            path = re.sub(r', methods=.*', '', path)
            func_name = r[2]
            login_req = '@login_required' in r[1]
            role = 'client' if "current_user.role != 'client'" in r[1] else 'architect' if 'require_architect' in r[1] else 'All'
            
            # Simple heuristic for returns
            body = content[content.find(f"def {func_name}("):]
            body = body[:body.find('\n@')] if '\n@' in body else body
            ret = 'redirect' if 'return redirect' in body else 'template' if 'render_template' in body else 'JSON' if 'jsonify' in body else 'unknown'
            
            yield f"{os.path.basename(f)} | `{path}` | {methods_str} | `{func_name}` | {login_req} | {role} | {ret}"

def generate_pass1():
    print("## ═══ PASS 1 — COMPLETE FILE & ROUTE INVENTORY ═══")
    print("\n### TABLE 1A — ALL FLASK ROUTES")
    print("| File | Decorator | HTTP Methods | Function Name | login_required? | Roles Allowed | Returns |")
    print("|---|---|---|---|---|---|---|")
    for r in find_routes():
        print(f"| {r} |")
    print("\nBased on source analysis.")

generate_pass1()

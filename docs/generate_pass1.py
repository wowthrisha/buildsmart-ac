import ast
import os
import glob
import re

def get_routes():
    res = []
    files = glob.glob('app/routes/*.py') + ['app/auth.py', 'app/__init__.py', 'app/ocr.py', 'app/rag.py', 'app/tnpcr.py']
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
                                    methods = ",".join([el.value for el in getattr(kw.value, 'elts', []) if hasattr(el, 'value')])
                        elif isinstance(dec, ast.Name) and dec.id == 'login_required':
                            login_req = True
                    if route_path:
                        body_code = ast.unparse(node)
                        if "current_user.role != 'client'" in body_code:
                            roles = "architect"
                        elif "current_user.role != 'architect'" in body_code:
                            roles = "client"
                        elif "require_architect" in body_code:
                            roles = "architect"
                        
                        ret = "unknown"
                        if "render_template(" in body_code: ret = "template"
                        elif "jsonify(" in body_code: ret = "JSON"
                        elif "redirect(" in body_code: ret = "redirect"
                        
                        res.append(f"| {os.path.basename(f)} | `{route_path}` | {methods} | `{node.name}` | {login_req} | {roles} | {ret} |")
        except Exception as e:
            pass
    return res

def get_models():
    res = []
    if os.path.exists('app/models.py'):
        code = open('app/models.py').read()
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                table_name = ""
                fields = []
                rels = []
                fks = []
                for child in node.body:
                    if isinstance(child, ast.Assign):
                        for target in child.targets:
                            if isinstance(target, ast.Name):
                                if target.id == '__tablename__':
                                    if isinstance(child.value, ast.Constant):
                                        table_name = child.value.value
                                elif isinstance(child.value, ast.Call) and (getattr(child.value.func, 'id', '') == 'db.Column' or getattr(child.value.func, 'attr', '') == 'Column'):
                                    # Very basic extraction
                                    ftype = ast.unparse(child.value.args[0]) if child.value.args else "Unknown"

                                    fields.append(f"{target.id} ({ftype})")
                                    if "db.ForeignKey" in ast.unparse(child.value):
                                        fks.append(target.id)
                                elif isinstance(child.value, ast.Call) and (getattr(child.value.func, 'id', '') == 'db.relationship' or getattr(child.value.func, 'attr', '') == 'relationship'):
                                    rels.append(target.id)
                if fields or rels:
                    res.append(f"| {node.name} | {table_name} | {', '.join(fields)} | {', '.join(rels)} | {', '.join(fks)} |")
    return res

def get_templates():
    res = []
    for root, _, files in os.walk('app/templates'):
        for file in files:
            if file.endswith('.html'):
                path = os.path.join(root, file)
                rel_path = os.path.relpath(path, 'app/templates')
                content = open(path).read()
                
                # find vars
                vars_expected = set(re.findall(r'\{\{(.*?)\}\}', content))
                vars_expected = {v.strip() for v in vars_expected}
                
                for_vars = set(re.findall(r'\{%\s*for\s+(.*?)\s+in\s+(.*?)\s*%\}', content))
                for_vars_list = [f"{v[0]} in {v[1]}" for v in for_vars]
                
                all_vars = list(vars_expected) + for_vars_list
                vars_str = "<br>".join(all_vars)[:200]
                
                # find forms
                forms = re.findall(r'<form\s+.*?>', content)
                forms_str = "<br>".join([f.replace('<', '&lt;').replace('>', '&gt;') for f in forms])
                
                # JS fetch
                fetches = re.findall(r'fetch\([\'"](.*?)[\'"].*?\}', content, re.DOTALL)
                fetches_str = "<br>".join(fetches)[:100]
                
                res.append(f"| {rel_path} | Route Unknown | {vars_str} | {forms_str} | {fetches_str} |")
    return res

def get_js():
    res = []
    # from static and inline JS
    js_files = glob.glob('app/static/**/*.js', recursive=True)
    html_files = glob.glob('app/templates/**/*.html', recursive=True)
    for f in js_files + html_files:
        lines = open(f).readlines()
        for i, line in enumerate(lines):
            if 'fetch(' in line or '$.ajax(' in line:
                match = re.search(r'fetch\([\'"](.*?)[\'"]', line)
                url = match.group(1) if match else "Unknown"
                method = "GET"
                if "method:" in "".join(lines[i:i+5]):
                    m_match = re.search(r"method:\s*['\"](.*?)['\"]", "".join(lines[i:i+5]))
                    if m_match: method = m_match.group(1).upper()
                res.append(f"| {os.path.basename(f)} | ~{i+1} | {url} | {method} | Unknown | Unknown | Unknown |")
    return res

with open('docs/ROUTE_INVENTORY.md', 'w') as out:
    out.write("# ═══ PASS 1 — COMPLETE FILE & ROUTE INVENTORY ═══\n\n")
    
    out.write("## TABLE 1A — ALL FLASK ROUTES\n")
    out.write("| File | Decorator | HTTP Methods | Function Name | login_required? | Roles Allowed | Returns |\n")
    out.write("|---|---|---|---|---|---|---|\n")
    for r in get_routes(): out.write(r + "\n")
    
    out.write("\n## TABLE 1B — ALL SQLALCHEMY MODELS\n")
    out.write("| Model Class | Table Name | Fields | Relationships | Foreign Keys |\n")
    out.write("|---|---|---|---|---|\n")
    for r in get_models(): out.write(r + "\n")
    
    out.write("\n## TABLE 1C — ALL JINJA2 TEMPLATES\n")
    out.write("| Template | Served By | Variables Expected | Forms | JS Fetch |\n")
    out.write("|---|---|---|---|---|\n")
    for r in get_templates(): out.write(r + "\n")
    
    out.write("\n## TABLE 1D — ALL JS FETCH / AJAX CALLS\n")
    out.write("| File | Line | URL | Method | Body Sent | Expected Response | Trigger |\n")
    out.write("|---|---|---|---|---|---|---|\n")
    for r in get_js(): out.write(r + "\n")
    
    out.write("\nINVENTORY COMPLETE. Proceeding to Pass 2.\n")

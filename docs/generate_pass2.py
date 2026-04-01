import ast
import os
import glob
import re

def get_flask_routes():
    routes = {}
    files = glob.glob('app/routes/*.py') + ['app/auth.py', 'app/__init__.py', 'app/ocr.py', 'app/rag.py', 'app/tnpcr.py']
    for f in files:
        if not os.path.exists(f): continue
        code = open(f).read()
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    route_path = None
                    methods = ["GET"]
                    for dec in node.decorator_list:
                        if isinstance(dec, ast.Call) and getattr(dec.func, 'attr', '') == 'route':
                            if dec.args:
                                route_path = str(dec.args[0].value)
                            for kw in dec.keywords:
                                if kw.arg == 'methods':
                                    methods = [el.value for el in getattr(kw.value, 'elts', []) if hasattr(el, 'value')]
                    if route_path:
                        body = ast.unparse(node)
                        inputs = []
                        if 'request.form' in body: inputs.append('form')
                        if 'request.json' in body or 'request.get_json()' in body: inputs.append('json')
                        if 'request.files' in body: inputs.append('files')
                        
                        ret = "template"
                        if "jsonify" in body or "request.get_json" in body: ret = "json"
                        elif "redirect" in body: ret = "redirect"
                        
                        # convert flask route to regex
                        route_regex = re.sub(r'<[^>]+>', '[^/]+', route_path)
                        routes[route_path] = {
                            "regex": "^" + route_regex + "$",
                            "methods": methods,
                            "inputs": inputs,
                            "returns": ret,
                            "file": f
                        }
        except:
            pass
    return routes

def find_mismatches(routes):
    mismatches = []
    html_files = glob.glob('app/templates/**/*.html', recursive=True)
    js_files = glob.glob('app/static/**/*.js', recursive=True)
    
    count = 1
    
    for f in html_files + js_files:
        lines = open(f).readlines()
        content = "".join(lines)
        
        # Check forms
        forms = re.findall(r'<form[^>]*action=[\'"]([^\'"]+)[\'"][^>]*method=[\'"]([^\'"]+)[\'"]', content, re.IGNORECASE)
        for url, method in forms:
            if url.startswith('{{') or url == '#':
                continue # ignore url_for dynamic urls for script simplification
            
            matched_route = None
            for rpath, rdata in routes.items():
                if re.match(rdata['regex'], url.split('?')[0]):
                    matched_route = rdata
                    break
            
            if not matched_route:
                mismatches.append(f"""╔══════════════════════════════════════════════╗
║ MISMATCH #{count}                                  ║
╠══════════════════════════════════════════════╣
║ Location       : {f}
║ Frontend calls : [{method.upper()}] {url}
║ Backend has    : MISSING — NO ROUTE FOUND
║ Mismatch type  : MISSING
║ Impact         : Form submission will 404
║ Fix            : Add the corresponding route or fix the action URL
╚══════════════════════════════════════════════╝""")
                count += 1
            elif method.upper() not in [m.upper() for m in matched_route['methods']]:
                mismatches.append(f"""╔══════════════════════════════════════════════╗
║ MISMATCH #{count}                                  ║
╠══════════════════════════════════════════════╣
║ Location       : {f}
║ Frontend calls : [{method.upper()}] {url}
║ Backend has    : {matched_route['methods']} for {url}
║ Mismatch type  : Method
║ Impact         : Form submission will 405 Method Not Allowed
║ Fix            : Add '{method.upper()}' to methods list in route decorator
╚══════════════════════════════════════════════╝""")
                count += 1

        # Check fetches
        for i, line in enumerate(lines):
            if 'fetch(' in line or '$.ajax(' in line:
                match = re.search(r'fetch\([\'"]([^\'"]+)[\'"]', line)
                if not match: continue
                url = match.group(1)
                
                method = "GET"
                block = "".join(lines[i:i+10])
                m_match = re.search(r"method:\s*['\"](.*?)['\"]", block)
                if m_match: method = m_match.group(1).upper()
                
                body_type = "none"
                if "FormData" in block: body_type = "form/files"
                elif "JSON.stringify" in block: body_type = "json"
                
                matched_route = None
                for rpath, rdata in routes.items():
                    if re.match(rdata['regex'], url.split('?')[0]):
                        matched_route = rdata
                        break
                
                if url.startswith('/'):
                    if not matched_route:
                        mismatches.append(f"""╔══════════════════════════════════════════════╗
║ MISMATCH #{count}                                  ║
╠══════════════════════════════════════════════╣
║ Location       : {f}, line ~{i+1}
║ Frontend calls : [{method}] {url}
║ Backend has    : MISSING — NO ROUTE FOUND
║ Mismatch type  : MISSING
║ Impact         : API call will 404
║ Fix            : Create the correct endpoint
╚══════════════════════════════════════════════╝""")
                        count += 1
                    else:
                        if method not in [m.upper() for m in matched_route['methods']]:
                            mismatches.append(f"""╔══════════════════════════════════════════════╗
║ MISMATCH #{count}                                  ║
╠══════════════════════════════════════════════╣
║ Location       : {f}, line ~{i+1}
║ Frontend calls : [{method}] {url}
║ Backend has    : {matched_route['methods']}
║ Mismatch type  : Method
║ Impact         : API call will 405 Method Not Allowed
║ Fix            : Allow {method} in the route decorator
╚══════════════════════════════════════════════╝""")
                            count += 1
                        
                        elif body_type == 'json' and 'json' not in matched_route['inputs']:
                            mismatches.append(f"""╔══════════════════════════════════════════════╗
║ MISMATCH #{count}                                  ║
╠══════════════════════════════════════════════╣
║ Location       : {f}, line ~{i+1}
║ Frontend calls : [{method}] {url} (JSON payload)
║ Backend has    : Does not read request.json
║ Mismatch type  : Body type
║ Impact         : Backend ignores sent JSON data
║ Fix            : Read payload via request.get_json()
╚══════════════════════════════════════════════╝""")
                            count += 1

    return mismatches

routes = get_flask_routes()
mismatches = find_mismatches(routes)

with open('docs/AUDIT_REPORT.md', 'w') as out:
    out.write("## ═══ PASS 2 — ENDPOINT MISMATCH AUDIT ═══\n\n")
    for m in mismatches:
        out.write(m + "\n\n")
    out.write(f"PASS 2 COMPLETE. {len(mismatches)} endpoint mismatches found.\n\n")

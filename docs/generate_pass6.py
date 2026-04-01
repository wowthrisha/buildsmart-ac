import os
import glob
import re

def perform_security_checklist():
    checks = {}
    
    # Check CSRF
    app_init = open('app/__init__.py').read() if os.path.exists('app/__init__.py') else ""
    checks['CSRF protection'] = 'PRESENT' if 'CSRFProtect' in app_init else 'MISSING'
    
    # Check File upload validation
    routes = "".join([open(f).read() for f in glob.glob('app/routes/*.py')])
    checks['File upload validation'] = 'PRESENT' if 'secure_filename' in routes else 'MISSING'
    
    # SQL injection (raw SQL instead of ORM)
    checks['SQL injection protection'] = 'PARTIAL' if 'execute(' in routes and 'text(' in routes else 'PRESENT'
    
    # XSS (safe filter without sanitization)
    templates = "".join([open(f).read() for f in glob.glob('app/templates/**/*.html', recursive=True)])
    checks['XSS protection'] = 'MISSING (uses |safe)' if '|safe' in templates else 'PRESENT'
    
    # Sensitive keys
    config = open('config.py').read() if os.path.exists('config.py') else app_init
    checks['Sensitive keys hardcoded'] = 'PRESENT' if 'SECRET_KEY = "' in config or 'mysql://' in config else 'MISSING (clean)'
    
    # DEBUG=True
    checks['DEBUG=True in config'] = 'PRESENT' if 'DEBUG = True' in config or 'debug=True' in config else 'MISSING'
    
    # Error pages
    checks['Custom Error pages'] = 'PRESENT' if os.path.exists('app/templates/errors/404.html') else 'MISSING'
    
    # Password hashing
    auth = open('app/auth.py').read() if os.path.exists('app/auth.py') else ""
    checks['Password hashing'] = 'PRESENT' if 'generate_password_hash' in auth or 'bcrypt' in auth else 'MISSING'
    
    return checks

def audit_error_handling():
    res = []
    files = glob.glob('app/routes/*.py') + ['app/auth.py']
    for f in files:
        if not os.path.exists(f): continue
        content = open(f).read()
        routes = re.findall(r'@(?:bp|app)\.route\((.*?)\)(.*?)(?:def (.*?)\():', content, re.DOTALL)
        for r in routes:
            path = r[0].strip('\'"')
            func_name = r[2]
            
            body = content[content.find(f"def {func_name}("):]
            body = body[:body.find('\n@')] if '\n@' in body else body
            
            has_try = 'try:' in body
            failure_mode = 'Returns JSON 500' if 'jsonify' in body and ('500' in body or '400' in body) else 'Raw exception / 500 HTML'
            user_sees = 'JSON error' if 'jsonify' in failure_mode else 'Crash page'
            fix = 'None' if has_try and user_sees == 'JSON error' else 'Add try/except returning JSON'
            
            res.append(f"| `{path}` | {'Yes' if has_try else 'No'} | {failure_mode} | {user_sees} | JSON error | {'Yes' if fix != 'None' else 'No'} |")
    return res

out = open('docs/AUDIT_REPORT.md', 'a')
out.write("## ═══ PASS 6 — SECURITY & ERROR HANDLING AUDIT ═══\n\n")

out.write("### 6A — SECURITY CHECKLIST\n")
checks = perform_security_checklist()
for k, v in checks.items():
    out.write(f"- [x] {k}: **{v}**\n")

out.write("\n### 6B — ERROR HANDLING AUDIT\n")
out.write("| Route | Has try/except | Failure mode | What user sees | Should be | Fix needed? |\n")
out.write("|---|---|---|---|---|---|\n")

err_audit = audit_error_handling()
for r in err_audit: out.write(r + "\n")

out.write(f"\nPASS 6 COMPLETE. Security issues and error handler gaps identified.\n\n")
out.close()

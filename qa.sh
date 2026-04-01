#!/bin/bash

export MYPYPATH=".:/Users/thrisha/BS_APP/buildsmart/venv_clean/lib/python3.13/site-packages"
export FLASK_APP=run.py
export DATABASE_URL="sqlite:////tmp/qa_$(date +%s).db"

echo "Starting Setup..."
rm -f /tmp/buildsmart.log
pkill -f "./venv_clean/bin/python3 run.py" 2>/dev/null || true
pkill -f "flask run" 2>/dev/null || true
sleep 1
PYTHONPATH="$MYPYPATH" ./venv_clean/bin/python3 run.py > /tmp/buildsmart.log 2>&1 &
sleep 5

# Seeding
cat > /tmp/seed.py << 'PYEOF'
from app import create_app, db
from app.models import User, Project, ComplianceItem
from werkzeug.security import generate_password_hash
app = create_app()
with app.app_context():
    arch = User.query.filter_by(email='arch@qa.com').first()
    if not arch:
        arch = User(name='QA Architect', email='arch@qa.com', password_hash=generate_password_hash('qapass123'), role='architect')
        db.session.add(arch)
        db.session.commit()
    
    client = User.query.filter_by(email='client@qa.com').first()
    if not client:
        client = User(name='QA Client', email='client@qa.com', password_hash=generate_password_hash('qapass123'), role='client')
        db.session.add(client)
        db.session.commit()

    proj = Project.query.filter_by(name='QA Test Project').first()
    if not proj:
        proj = Project(name='QA Test Project', architect_id=arch.id, client_id=client.id, total_budget=500100, plot_zone='Residential')
        db.session.add(proj)
        db.session.commit()
        for label in ['Building Plan Approval','Fire NOC']:
            db.session.add(ComplianceItem(project_id=proj.id, label=label))
        db.session.commit()
PYEOF
PYTHONPATH="$MYPYPATH" ./venv_clean/bin/python3 /tmp/seed.py

ARCH_ID=$(PYTHONPATH="$MYPYPATH" ./venv_clean/bin/python3 -c "from app import create_app; from app.models import User; create_app().app_context().push(); u=User.query.filter_by(email='arch@qa.com').first(); print(u.id if u else '')")
CLIENT_ID=$(PYTHONPATH="$MYPYPATH" ./venv_clean/bin/python3 -c "from app import create_app; from app.models import User; create_app().app_context().push(); u=User.query.filter_by(email='client@qa.com').first(); print(u.id if u else '')")
PROJECT_ID=$(PYTHONPATH="$MYPYPATH" ./venv_clean/bin/python3 -c "from app import create_app; from app.models import Project; create_app().app_context().push(); p=Project.query.filter_by(name='QA Test Project').first(); print(p.id if p else '')")
COMP_ID=$(PYTHONPATH="$MYPYPATH" ./venv_clean/bin/python3 -c "from app import create_app; from app.models import ComplianceItem; create_app().app_context().push(); c=ComplianceItem.query.filter_by(project_id='$PROJECT_ID').first(); print(c.id if c else '')")

# Robust CSRF Extraction from META tag
get_arch_csrf() {
    curl -s -b /tmp/arch.cookies http://127.0.0.1:5001/dashboard | grep "csrf-token" | sed 's/.*content="\([^"]*\)".*/\1/' | head -n 1
}
get_client_csrf() {
    curl -s -b /tmp/client.cookies http://127.0.0.1:5001/my_project/ | grep "csrf-token" | sed 's/.*content="\([^"]*\)".*/\1/' | head -n 1
}

echo "Running Login/Auth Tests..."
# Login Architect
CSRF=$(curl -s -c /tmp/arch.cookies http://127.0.0.1:5001/login | grep "csrf_token" | sed 's/.*value="\([^"]*\)".*/\1/')
curl -s -b /tmp/arch.cookies -c /tmp/arch.cookies -d "csrf_token=$CSRF" -d "email=arch@qa.com" -d "password=qapass123" -L http://127.0.0.1:5001/login -o /tmp/arch_home.html
grep -qi "Dashboard\|Logout" /tmp/arch_home.html && echo "✅ 1.2 Architect login successful" || echo "❌ 1.2 Architect login FAILED"

# Login Client
CSRF=$(curl -s -c /tmp/client.cookies http://127.0.0.1:5001/login | grep "csrf_token" | sed 's/.*value="\([^"]*\)".*/\1/')
curl -s -b /tmp/client.cookies -c /tmp/client.cookies -d "csrf_token=$CSRF" -d "email=client@qa.com" -d "password=qapass123" -L http://127.0.0.1:5001/login -o /tmp/client_portal.html
grep -qi "Portal\|Logout" /tmp/client_portal.html && echo "✅ 1.3 Client login successful" || echo "❌ 1.3 Client login FAILED"

# 1.5 Registration Role Enforcement
REG_CSRF=$(curl -s -c /tmp/reg.cookies http://127.0.0.1:5001/register | grep "csrf_token" | sed 's/.*value="\([^"]*\)".*/\1/')
curl -s -b /tmp/reg.cookies -c /tmp/reg.cookies -d "csrf_token=$REG_CSRF" -d "name=Hacker" -d "email=hacker@qa.com" -d "password=hack123" -d "role=architect" -L http://127.0.0.1:5001/register -o /dev/null
ROLE=$(PYTHONPATH="$MYPYPATH" ./venv_clean/bin/python3 -c "from app import create_app; from app.models import User; create_app().app_context().push(); u = User.query.filter_by(email='hacker@qa.com').first(); print(u.role if u else 'NONE')")
[ "$ROLE" == "client" ] && echo "✅ 1.5 Registration forced to client" || echo "❌ 1.5 Registration role=$ROLE"

echo "Running Functional Tests (Architect)..."
# 3.1 Create Project
CSRF=$(get_arch_csrf)
[ -z "$CSRF" ] && echo "❌ CSRF empty"
curl -s -b /tmp/arch.cookies -c /tmp/arch.cookies -d "csrf_token=$CSRF" -d "name=QA+Project+2" -d "client_id=$CLIENT_ID" -d "plot_zone=Residential" -L http://127.0.0.1:5001/projects/create -o /dev/null
PYTHONPATH="$MYPYPATH" ./venv_clean/bin/python3 -c "from app import create_app; from app.models import Project; create_app().app_context().push(); p = Project.query.filter_by(name='QA Project 2').first(); assert p is not None; print('✅ 3.1 Create Project successful')"

# 3.3 Update Budget
CSRF=$(get_arch_csrf)
curl -s -b /tmp/arch.cookies -c /tmp/arch.cookies -d "csrf_token=$CSRF" -d "total_budget=750010" -L "http://127.0.0.1:5001/projects/$PROJECT_ID/payments/budget" -o /dev/null
BUDGET=$(PYTHONPATH="$MYPYPATH" ./venv_clean/bin/python3 -c "from app import create_app; from app.models import Project; create_app().app_context().push(); p = Project.query.get($PROJECT_ID); print(p.total_budget)")
[ "$BUDGET" == "750010.0" ] && echo "✅ 3.3 Update budget successful" || echo "❌ 3.3 Update budget FAILED ($BUDGET)"

# 3.4 Add custom compliance
CSRF=$(get_arch_csrf)
curl -s -b /tmp/arch.cookies -c /tmp/arch.cookies -d "csrf_token=$CSRF" -d "label=Custom+Cert" -L "http://127.0.0.1:5001/projects/$PROJECT_ID/compliance/add-custom" -o /dev/null
PYTHONPATH="$MYPYPATH" ./venv_clean/bin/python3 -c "from app import create_app; from app.models import ComplianceItem; create_app().app_context().push(); c = ComplianceItem.query.filter_by(label='Custom Cert').first(); assert c is not None; print('✅ 3.4 Custom compliance success')"

# 3.5 Toggle
CSRF=$(get_arch_csrf)
curl -s -b /tmp/arch.cookies -c /tmp/arch.cookies -H "X-CSRFToken: $CSRF" -X POST "http://127.0.0.1:5001/projects/$PROJECT_ID/compliance/$COMP_ID/toggle" -o /tmp/toggle.json
grep -q "arch_checked\": true" /tmp/toggle.json && echo "✅ 3.5 Compliance toggle successful" || echo "❌ 3.5 Toggle FAILED"

# 3.7 Upload .py (Rejected)
echo "evil" > /tmp/malicious.py
CSRF=$(get_arch_csrf)
curl -s -b /tmp/arch.cookies -c /tmp/arch.cookies -F "csrf_token=$CSRF" -F "doc=@/tmp/malicious.py" -L "http://127.0.0.1:5001/projects/$PROJECT_ID/documents/upload" -o /tmp/reject.html
grep -qi "not allowed\|extension\|invalid\|error" /tmp/reject.html && echo "✅ 3.7 Upload .py REJECTED (Security Passed)" || echo "❌ 3.7 Upload .py NOT REJECTED"

echo "Running Functional Tests (Client)..."
# 4.1 Client Toggle
CSRF=$(get_client_csrf)
curl -s -b /tmp/client.cookies -c /tmp/client.cookies -H "X-CSRFToken: $CSRF" -X POST "http://127.0.0.1:5001/projects/$PROJECT_ID/compliance/$COMP_ID/toggle" -o /tmp/toggle_cl.json
grep -q "client_checked\": true" /tmp/toggle_cl.json && echo "✅ 4.1 Client toggle successful" || echo "❌ 4.1 Client toggle FAILED"

# 5.1/5.2 Security Headers
HEADERS=$(curl -s -I http://127.0.0.1:5001/login)
echo "$HEADERS" | grep -qi "HttpOnly" && echo "✅ 5.1 HttpOnly flag present" || echo "❌ 5.1 HttpOnly flag MISSING"
echo "$HEADERS" | grep -qi "SameSite=Lax" && echo "✅ 5.2 SameSite=Lax present" || echo "❌ 5.2 SameSite flag MISSING"

# 5.3 Blind POST
CODE=$(curl -s -b /tmp/arch.cookies -X POST http://127.0.0.1:5001/projects/create -d "name=Hack" -o /dev/null -w "%{http_code}")
[ "$CODE" == "400" ] && echo "✅ 5.3 POST without CSRF blocked" || echo "❌ 5.3 POST without CSRF allowed ($CODE)"

echo "Done."

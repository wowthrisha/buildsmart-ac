#!/bin/bash
PORT=5000
BASE="http://127.0.0.1:$PORT"
export MYPYPATH=".:$(pwd)/myenv"
export DATABASE_URL="sqlite:////tmp/audit_curl_$(date +%s).db"

echo "--- STARTING LIVE AUDIT VERIFICATION ---"

# 0. Seed
cat > /tmp/seed_audit.py << 'PYEOF'
from app import create_app, db
from app.models import User, Project, ComplianceItem
from werkzeug.security import generate_password_hash
app = create_app()
with app.app_context():
    db.create_all()
    a = User(name='Arch', email='arch@qa.com', password_hash=generate_password_hash('qapass123'), role='architect')
    c = User(name='Client', email='client@qa.com', password_hash=generate_password_hash('qapass123'), role='client')
    db.session.add_all([a, c])
    db.session.commit()
    p = Project(name='Audit Project', architect_id=a.id, client_id=c.id)
    db.session.add(p)
    db.session.commit()
PYEOF
PYTHONPATH="$MYPYPATH" venv_clean/bin/python /tmp/seed_audit.py

# 1. Start App
pkill -f "run.py" 2>/dev/null
PYTHONPATH="$MYPYPATH" venv_clean/bin/python run.py > /tmp/audit_run.log 2>&1 &
sleep 5

# Confirm running
CODE=$(curl -s -o /dev/null -w "%{http_code}" $BASE/login)
if [ "$CODE" == "200" ]; then
  echo "✅ App running on $PORT"
else
  echo "❌ App NOT running ($CODE). Check /tmp/audit_run.log"
  exit 1
fi

# 2. Architect Login
CSRF=$(curl -s -c /tmp/a.jar $BASE/login | grep "csrf_token" | sed 's/.*value="\([^"]*\)".*/\1/' | head -1)
curl -s -b /tmp/a.jar -c /tmp/a.jar \
  -d "csrf_token=$CSRF&email=arch@qa.com&password=qapass123" \
  -L $BASE/login -o /tmp/arch.html
grep -qi "Logout\|Dashboard" /tmp/arch.html \
  && echo "✅ Arch login" || echo "❌ Arch login"

# 3. Client Login
CSRF=$(curl -s -c /tmp/c.jar $BASE/login | grep "csrf_token" | sed 's/.*value="\([^"]*\)".*/\1/' | head -1)
curl -s -b /tmp/c.jar -c /tmp/c.jar \
  -d "csrf_token=$CSRF&email=client@qa.com&password=qapass123" \
  -L $BASE/login -o /tmp/client.html
grep -qi "Logout\|Portal\|my_project" /tmp/client.html \
  && echo "✅ Client login" || echo "❌ Client login"

# 4. Role boundary
echo "Checking role boundaries..."
for path in /dashboard /projects /compliance /payments /meetings /documents /plot /activity; do
  CODE=$(curl -s -b /tmp/c.jar -o /dev/null -w "%{http_code}" $BASE$path)
  [ "$CODE" == "403" ] && echo "✅ Client blocked from $path" || echo "❌ Client reached $path → $CODE"
done

# 5. Architect blocked from client area
CODE=$(curl -s -b /tmp/a.jar -o /dev/null -w "%{http_code}" $BASE/my_project/)
[ "$CODE" == "403" ] && echo "✅ Arch blocked from /my_project/" || echo "❌ $CODE"

# 6. Every architect page loads
echo "Checking architect routes..."
for path in /dashboard /projects /compliance /payments /meetings /documents /plot /activity /settings; do
  CODE=$(curl -s -b /tmp/a.jar -o /dev/null -w "%{http_code}" $BASE$path)
  [ "$CODE" == "200" ] && echo "✅ GET $path → 200" || echo "❌ GET $path → $CODE"
done

# 7. Every client page loads
echo "Checking client routes..."
for path in /my_project/ /my_project/documents /my_project/payments /my_project/meetings /my_project/plot; do
  CODE=$(curl -s -b /tmp/c.jar -o /dev/null -w "%{http_code}" $BASE$path)
  [ "$CODE" == "200" ] && echo "✅ GET $path → 200" || echo "❌ GET $path → $CODE"
done

# 8. CSRF enforcement
CODE=$(curl -s -b /tmp/a.jar -X POST $BASE/projects/create -d "name=Hack" -o /dev/null -w "%{http_code}")
[ "$CODE" == "400" ] || [ "$CODE" == "403" ] \
  && echo "✅ POST without CSRF blocked → $CODE" \
  || echo "❌ POST without CSRF allowed → $CODE"

# 9. File upload rejection
echo "evil()" > /tmp/bad.py
CSRF=$(curl -s -b /tmp/a.jar $BASE/projects/1 | grep 'name="csrf-token"' | sed 's/.*content="\([^"]*\)".*/\1/' | head -1)
[ -z "$CSRF" ] && CSRF=$(curl -s -b /tmp/a.jar $BASE/projects/1 | grep 'name="csrf_token"' | sed 's/.*value="\([^"]*\)".*/\1/' | head -1)

curl -s -L -b /tmp/a.jar \
  -F "csrf_token=$CSRF" -F "file=@/tmp/bad.py" \
  $BASE/projects/1/documents/upload -o /tmp/rej.html
grep -qi "not allowed\|extension\|invalid\|error" /tmp/rej.html \
  && echo "✅ .py upload rejected" || echo "❌ .py upload NOT rejected"

pkill -f "run.py"
echo "--- AUDIT VERIFICATION FINISHED ---"

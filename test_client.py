import urllib.request, re
from http.cookiejar import CookieJar
cj = CookieJar()
o = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
q = urllib.request.Request('http://127.0.0.1:5002/login', headers={'X-Forwarded-For': '192.168.1.105'})
r = o.open(q)
t = re.search(r'name="csrf_token" value="([^"]+)', r.read().decode()).group(1)
req = urllib.request.Request('http://127.0.0.1:5002/login', b'email=client@qa.com&password=qapass123&csrf_token='+t.encode(), {'Content-Type': 'application/x-www-form-urlencoded', 'X-Forwarded-For': '192.168.1.105'})
o.open(req)
try:
    r2 = o.open(urllib.request.Request('http://127.0.0.1:5002/my_project/', headers={'X-Forwarded-For': '192.168.1.105'}))
    print(r2.read().decode())
except Exception as e:
    print(e.read().decode() if hasattr(e, 'read') else str(e))

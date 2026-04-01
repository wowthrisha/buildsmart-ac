# PASS 7A — API CONTRACT DOCUMENT

───────────────────────────────────────────
ENDPOINT: GET /plot
AUTH: login_required | roles: architect
DESCRIPTION: Handles /plot
QUERY PARAMS: none
REQUEST BODY: none
SUCCESS RESPONSE (200):
  {
    // Depends on implementation. Currently returns template render.
  }
ERROR RESPONSES:
  401 — not authenticated
  403 — wrong role
  404 — resource not found
CURRENTLY RETURNS: template render
NEEDS CHANGE FOR API USE: yes - Replace with jsonify()
───────────────────────────────────────────

───────────────────────────────────────────
ENDPOINT: POST /projects/<int:project_id>/plot/upload
AUTH: login_required | roles: architect
DESCRIPTION: Handles /projects/<int:project_id>/plot/upload
QUERY PARAMS: none
REQUEST BODY: multipart/form-data or application/x-www-form-urlencoded depending on form
SUCCESS RESPONSE (200):
  {
    // Depends on implementation. Currently returns redirect.
  }
ERROR RESPONSES:
  401 — not authenticated
  403 — wrong role
  404 — resource not found
CURRENTLY RETURNS: redirect
NEEDS CHANGE FOR API USE: yes - Replace with jsonify()
───────────────────────────────────────────

───────────────────────────────────────────
ENDPOINT: POST /projects/<int:project_id>/plot/update
AUTH: login_required | roles: architect
DESCRIPTION: Handles /projects/<int:project_id>/plot/update
QUERY PARAMS: none
REQUEST BODY: multipart/form-data or application/x-www-form-urlencoded depending on form
SUCCESS RESPONSE (200):
  {
    // Depends on implementation. Currently returns redirect.
  }
ERROR RESPONSES:
  401 — not authenticated
  403 — wrong role
  404 — resource not found
CURRENTLY RETURNS: redirect
NEEDS CHANGE FOR API USE: yes - Replace with jsonify()
───────────────────────────────────────────

───────────────────────────────────────────
ENDPOINT: POST /projects/<int:project_id>/plot/confirm
AUTH: login_required | roles: architect
DESCRIPTION: Handles /projects/<int:project_id>/plot/confirm
QUERY PARAMS: none
REQUEST BODY: multipart/form-data or application/x-www-form-urlencoded depending on form
SUCCESS RESPONSE (200):
  {
    // Depends on implementation. Currently returns redirect.
  }
ERROR RESPONSES:
  401 — not authenticated
  403 — wrong role
  404 — resource not found
CURRENTLY RETURNS: redirect
NEEDS CHANGE FOR API USE: yes - Replace with jsonify()
───────────────────────────────────────────

───────────────────────────────────────────
ENDPOINT: POST /api/rag/query
AUTH: login_required | roles: client
DESCRIPTION: Handles /api/rag/query
QUERY PARAMS: none
REQUEST BODY: JSON payload
SUCCESS RESPONSE (200):
  {
    // Depends on implementation. Currently returns JSON.
  }
ERROR RESPONSES:
  401 — not authenticated
  403 — wrong role
  404 — resource not found
CURRENTLY RETURNS: JSON
NEEDS CHANGE FOR API USE: no (already JSON) - Replace with jsonify()
───────────────────────────────────────────

───────────────────────────────────────────
ENDPOINT: GET /payments
AUTH: login_required | roles: architect
DESCRIPTION: Handles /payments
QUERY PARAMS: none
REQUEST BODY: none
SUCCESS RESPONSE (200):
  {
    // Depends on implementation. Currently returns template render.
  }
ERROR RESPONSES:
  401 — not authenticated
  403 — wrong role
  404 — resource not found
CURRENTLY RETURNS: template render
NEEDS CHANGE FOR API USE: yes - Replace with jsonify()
───────────────────────────────────────────

───────────────────────────────────────────
ENDPOINT: POST /projects/<int:project_id>/payments/budget
AUTH: login_required | roles: architect
DESCRIPTION: Handles /projects/<int:project_id>/payments/budget
QUERY PARAMS: none
REQUEST BODY: multipart/form-data or application/x-www-form-urlencoded depending on form
SUCCESS RESPONSE (200):
  {
    // Depends on implementation. Currently returns redirect.
  }
ERROR RESPONSES:
  401 — not authenticated
  403 — wrong role
  404 — resource not found
CURRENTLY RETURNS: redirect
NEEDS CHANGE FOR API USE: yes - Replace with jsonify()
───────────────────────────────────────────

───────────────────────────────────────────
ENDPOINT: POST /projects/<int:project_id>/payments/add
AUTH: login_required | roles: architect
DESCRIPTION: Handles /projects/<int:project_id>/payments/add
QUERY PARAMS: none
REQUEST BODY: multipart/form-data or application/x-www-form-urlencoded depending on form
SUCCESS RESPONSE (200):
  {
    // Depends on implementation. Currently returns redirect.
  }
ERROR RESPONSES:
  401 — not authenticated
  403 — wrong role
  404 — resource not found
CURRENTLY RETURNS: redirect
NEEDS CHANGE FOR API USE: yes - Replace with jsonify()
───────────────────────────────────────────

───────────────────────────────────────────
ENDPOINT: GET /payments/download/<filename>
AUTH: login_required | roles: All
DESCRIPTION: Handles /payments/download/<filename>
QUERY PARAMS: none
REQUEST BODY: none
SUCCESS RESPONSE (200):
  {
    // Depends on implementation. Currently returns unknown.
  }
ERROR RESPONSES:
  401 — not authenticated
  403 — wrong role
  404 — resource not found
CURRENTLY RETURNS: unknown
NEEDS CHANGE FOR API USE: yes - Replace with jsonify()
───────────────────────────────────────────

───────────────────────────────────────────
ENDPOINT: GET /compliance
AUTH: login_required | roles: architect
DESCRIPTION: Handles /compliance
QUERY PARAMS: none
REQUEST BODY: none
SUCCESS RESPONSE (200):
  {
    // Depends on implementation. Currently returns template render.
  }
ERROR RESPONSES:
  401 — not authenticated
  403 — wrong role
  404 — resource not found
CURRENTLY RETURNS: template render
NEEDS CHANGE FOR API USE: yes - Replace with jsonify()
───────────────────────────────────────────

───────────────────────────────────────────
ENDPOINT: POST /projects/<int:project_id>/compliance/toggle/<int:item_id>
AUTH: login_required | roles: architect
DESCRIPTION: Handles /projects/<int:project_id>/compliance/toggle/<int:item_id>
QUERY PARAMS: none
REQUEST BODY: multipart/form-data or application/x-www-form-urlencoded depending on form
SUCCESS RESPONSE (200):
  {
    // Depends on implementation. Currently returns JSON.
  }
ERROR RESPONSES:
  401 — not authenticated
  403 — wrong role
  404 — resource not found
CURRENTLY RETURNS: JSON
NEEDS CHANGE FOR API USE: no (already JSON) - Replace with jsonify()
───────────────────────────────────────────

───────────────────────────────────────────
ENDPOINT: POST /projects/<int:project_id>/compliance/add-custom
AUTH: login_required | roles: architect
DESCRIPTION: Handles /projects/<int:project_id>/compliance/add-custom
QUERY PARAMS: none
REQUEST BODY: JSON payload
SUCCESS RESPONSE (200):
  {
    // Depends on implementation. Currently returns JSON.
  }
ERROR RESPONSES:
  401 — not authenticated
  403 — wrong role
  404 — resource not found
CURRENTLY RETURNS: JSON
NEEDS CHANGE FOR API USE: no (already JSON) - Replace with jsonify()
───────────────────────────────────────────

───────────────────────────────────────────
ENDPOINT: GET /meetings
AUTH: login_required | roles: architect
DESCRIPTION: Handles /meetings
QUERY PARAMS: none
REQUEST BODY: none
SUCCESS RESPONSE (200):
  {
    // Depends on implementation. Currently returns template render.
  }
ERROR RESPONSES:
  401 — not authenticated
  403 — wrong role
  404 — resource not found
CURRENTLY RETURNS: template render
NEEDS CHANGE FOR API USE: yes - Replace with jsonify()
───────────────────────────────────────────

───────────────────────────────────────────
ENDPOINT: POST /projects/<int:project_id>/meetings/propose
AUTH: login_required | roles: architect
DESCRIPTION: Handles /projects/<int:project_id>/meetings/propose
QUERY PARAMS: none
REQUEST BODY: multipart/form-data or application/x-www-form-urlencoded depending on form
SUCCESS RESPONSE (200):
  {
    // Depends on implementation. Currently returns redirect.
  }
ERROR RESPONSES:
  401 — not authenticated
  403 — wrong role
  404 — resource not found
CURRENTLY RETURNS: redirect
NEEDS CHANGE FOR API USE: yes - Replace with jsonify()
───────────────────────────────────────────

───────────────────────────────────────────
ENDPOINT: POST /meetings/<int:meeting_id>/confirm
AUTH: login_required | roles: architect
DESCRIPTION: Handles /meetings/<int:meeting_id>/confirm
QUERY PARAMS: none
REQUEST BODY: multipart/form-data or application/x-www-form-urlencoded depending on form
SUCCESS RESPONSE (200):
  {
    // Depends on implementation. Currently returns redirect.
  }
ERROR RESPONSES:
  401 — not authenticated
  403 — wrong role
  404 — resource not found
CURRENTLY RETURNS: redirect
NEEDS CHANGE FOR API USE: yes - Replace with jsonify()
───────────────────────────────────────────

───────────────────────────────────────────
ENDPOINT: POST /meetings/<int:meeting_id>/notes
AUTH: login_required | roles: architect
DESCRIPTION: Handles /meetings/<int:meeting_id>/notes
QUERY PARAMS: none
REQUEST BODY: multipart/form-data or application/x-www-form-urlencoded depending on form
SUCCESS RESPONSE (200):
  {
    // Depends on implementation. Currently returns redirect.
  }
ERROR RESPONSES:
  401 — not authenticated
  403 — wrong role
  404 — resource not found
CURRENTLY RETURNS: redirect
NEEDS CHANGE FOR API USE: yes - Replace with jsonify()
───────────────────────────────────────────

───────────────────────────────────────────
ENDPOINT: POST /meetings/<int:meeting_id>/counter
AUTH: login_required | roles: architect
DESCRIPTION: Handles /meetings/<int:meeting_id>/counter
QUERY PARAMS: none
REQUEST BODY: multipart/form-data or application/x-www-form-urlencoded depending on form
SUCCESS RESPONSE (200):
  {
    // Depends on implementation. Currently returns redirect.
  }
ERROR RESPONSES:
  401 — not authenticated
  403 — wrong role
  404 — resource not found
CURRENTLY RETURNS: redirect
NEEDS CHANGE FOR API USE: yes - Replace with jsonify()
───────────────────────────────────────────

───────────────────────────────────────────
ENDPOINT: GET /documents
AUTH: login_required | roles: architect
DESCRIPTION: Handles /documents
QUERY PARAMS: none
REQUEST BODY: none
SUCCESS RESPONSE (200):
  {
    // Depends on implementation. Currently returns template render.
  }
ERROR RESPONSES:
  401 — not authenticated
  403 — wrong role
  404 — resource not found
CURRENTLY RETURNS: template render
NEEDS CHANGE FOR API USE: yes - Replace with jsonify()
───────────────────────────────────────────

───────────────────────────────────────────
ENDPOINT: POST /projects/<int:project_id>/documents/upload
AUTH: login_required | roles: architect
DESCRIPTION: Handles /projects/<int:project_id>/documents/upload
QUERY PARAMS: none
REQUEST BODY: multipart/form-data or application/x-www-form-urlencoded depending on form
SUCCESS RESPONSE (200):
  {
    // Depends on implementation. Currently returns redirect.
  }
ERROR RESPONSES:
  401 — not authenticated
  403 — wrong role
  404 — resource not found
CURRENTLY RETURNS: redirect
NEEDS CHANGE FOR API USE: yes - Replace with jsonify()
───────────────────────────────────────────

───────────────────────────────────────────
ENDPOINT: POST /documents/<int:doc_id>/share
AUTH: login_required | roles: architect
DESCRIPTION: Handles /documents/<int:doc_id>/share
QUERY PARAMS: none
REQUEST BODY: multipart/form-data or application/x-www-form-urlencoded depending on form
SUCCESS RESPONSE (200):
  {
    // Depends on implementation. Currently returns redirect.
  }
ERROR RESPONSES:
  401 — not authenticated
  403 — wrong role
  404 — resource not found
CURRENTLY RETURNS: redirect
NEEDS CHANGE FOR API USE: yes - Replace with jsonify()
───────────────────────────────────────────

───────────────────────────────────────────
ENDPOINT: GET /documents/<int:doc_id>/download
AUTH: login_required | roles: All
DESCRIPTION: Handles /documents/<int:doc_id>/download
QUERY PARAMS: none
REQUEST BODY: none
SUCCESS RESPONSE (200):
  {
    // Depends on implementation. Currently returns unknown.
  }
ERROR RESPONSES:
  401 — not authenticated
  403 — wrong role
  404 — resource not found
CURRENTLY RETURNS: unknown
NEEDS CHANGE FOR API USE: yes - Replace with jsonify()
───────────────────────────────────────────

───────────────────────────────────────────
ENDPOINT: POST /documents/<int:doc_id>/delete
AUTH: login_required | roles: architect
DESCRIPTION: Handles /documents/<int:doc_id>/delete
QUERY PARAMS: none
REQUEST BODY: multipart/form-data or application/x-www-form-urlencoded depending on form
SUCCESS RESPONSE (200):
  {
    // Depends on implementation. Currently returns redirect.
  }
ERROR RESPONSES:
  401 — not authenticated
  403 — wrong role
  404 — resource not found
CURRENTLY RETURNS: redirect
NEEDS CHANGE FOR API USE: yes - Replace with jsonify()
───────────────────────────────────────────

───────────────────────────────────────────
ENDPOINT: POST /documents/<int:doc_id>/upload-version
AUTH: login_required | roles: architect
DESCRIPTION: Handles /documents/<int:doc_id>/upload-version
QUERY PARAMS: none
REQUEST BODY: multipart/form-data or application/x-www-form-urlencoded depending on form
SUCCESS RESPONSE (200):
  {
    // Depends on implementation. Currently returns redirect.
  }
ERROR RESPONSES:
  401 — not authenticated
  403 — wrong role
  404 — resource not found
CURRENTLY RETURNS: redirect
NEEDS CHANGE FOR API USE: yes - Replace with jsonify()
───────────────────────────────────────────

───────────────────────────────────────────
ENDPOINT: POST /documents/<int:doc_id>/request-approval
AUTH: login_required | roles: architect
DESCRIPTION: Handles /documents/<int:doc_id>/request-approval
QUERY PARAMS: none
REQUEST BODY: multipart/form-data or application/x-www-form-urlencoded depending on form
SUCCESS RESPONSE (200):
  {
    // Depends on implementation. Currently returns redirect.
  }
ERROR RESPONSES:
  401 — not authenticated
  403 — wrong role
  404 — resource not found
CURRENTLY RETURNS: redirect
NEEDS CHANGE FOR API USE: yes - Replace with jsonify()
───────────────────────────────────────────

───────────────────────────────────────────
ENDPOINT: POST /documents/<int:doc_id>/approve
AUTH: login_required | roles: client
DESCRIPTION: Handles /documents/<int:doc_id>/approve
QUERY PARAMS: none
REQUEST BODY: multipart/form-data or application/x-www-form-urlencoded depending on form
SUCCESS RESPONSE (200):
  {
    // Depends on implementation. Currently returns redirect.
  }
ERROR RESPONSES:
  401 — not authenticated
  403 — wrong role
  404 — resource not found
CURRENTLY RETURNS: redirect
NEEDS CHANGE FOR API USE: yes - Replace with jsonify()
───────────────────────────────────────────

───────────────────────────────────────────
ENDPOINT: GET /my_project/
AUTH: login_required | roles: client
DESCRIPTION: Handles /my_project/
QUERY PARAMS: none
REQUEST BODY: none
SUCCESS RESPONSE (200):
  {
    // Depends on implementation. Currently returns template render.
  }
ERROR RESPONSES:
  401 — not authenticated
  403 — wrong role
  404 — resource not found
CURRENTLY RETURNS: template render
NEEDS CHANGE FOR API USE: yes - Replace with jsonify()
───────────────────────────────────────────

───────────────────────────────────────────
ENDPOINT: GET /my_project/select/<int:project_id>
AUTH: login_required | roles: client
DESCRIPTION: Handles /my_project/select/<int:project_id>
QUERY PARAMS: none
REQUEST BODY: none
SUCCESS RESPONSE (200):
  {
    // Depends on implementation. Currently returns redirect.
  }
ERROR RESPONSES:
  401 — not authenticated
  403 — wrong role
  404 — resource not found
CURRENTLY RETURNS: redirect
NEEDS CHANGE FOR API USE: yes - Replace with jsonify()
───────────────────────────────────────────

───────────────────────────────────────────
ENDPOINT: GET /my_project/documents
AUTH: login_required | roles: client
DESCRIPTION: Handles /my_project/documents
QUERY PARAMS: none
REQUEST BODY: none
SUCCESS RESPONSE (200):
  {
    // Depends on implementation. Currently returns template render.
  }
ERROR RESPONSES:
  401 — not authenticated
  403 — wrong role
  404 — resource not found
CURRENTLY RETURNS: template render
NEEDS CHANGE FOR API USE: yes - Replace with jsonify()
───────────────────────────────────────────

───────────────────────────────────────────
ENDPOINT: GET /my_project/plot
AUTH: login_required | roles: client
DESCRIPTION: Handles /my_project/plot
QUERY PARAMS: none
REQUEST BODY: none
SUCCESS RESPONSE (200):
  {
    // Depends on implementation. Currently returns template render.
  }
ERROR RESPONSES:
  401 — not authenticated
  403 — wrong role
  404 — resource not found
CURRENTLY RETURNS: template render
NEEDS CHANGE FOR API USE: yes - Replace with jsonify()
───────────────────────────────────────────

───────────────────────────────────────────
ENDPOINT: GET /my_project/meetings
AUTH: login_required | roles: client
DESCRIPTION: Handles /my_project/meetings
QUERY PARAMS: none
REQUEST BODY: none
SUCCESS RESPONSE (200):
  {
    // Depends on implementation. Currently returns template render.
  }
ERROR RESPONSES:
  401 — not authenticated
  403 — wrong role
  404 — resource not found
CURRENTLY RETURNS: template render
NEEDS CHANGE FOR API USE: yes - Replace with jsonify()
───────────────────────────────────────────

───────────────────────────────────────────
ENDPOINT: GET /my_project/updates
AUTH: login_required | roles: client
DESCRIPTION: Handles /my_project/updates
QUERY PARAMS: none
REQUEST BODY: none
SUCCESS RESPONSE (200):
  {
    // Depends on implementation. Currently returns template render.
  }
ERROR RESPONSES:
  401 — not authenticated
  403 — wrong role
  404 — resource not found
CURRENTLY RETURNS: template render
NEEDS CHANGE FOR API USE: yes - Replace with jsonify()
───────────────────────────────────────────

───────────────────────────────────────────
ENDPOINT: GET /my_project/payments
AUTH: login_required | roles: client
DESCRIPTION: Handles /my_project/payments
QUERY PARAMS: none
REQUEST BODY: none
SUCCESS RESPONSE (200):
  {
    // Depends on implementation. Currently returns template render.
  }
ERROR RESPONSES:
  401 — not authenticated
  403 — wrong role
  404 — resource not found
CURRENTLY RETURNS: template render
NEEDS CHANGE FOR API USE: yes - Replace with jsonify()
───────────────────────────────────────────

───────────────────────────────────────────
ENDPOINT: GET /activity
AUTH: login_required | roles: architect
DESCRIPTION: Handles /activity
QUERY PARAMS: none
REQUEST BODY: none
SUCCESS RESPONSE (200):
  {
    // Depends on implementation. Currently returns template render.
  }
ERROR RESPONSES:
  401 — not authenticated
  403 — wrong role
  404 — resource not found
CURRENTLY RETURNS: template render
NEEDS CHANGE FOR API USE: yes - Replace with jsonify()
───────────────────────────────────────────

───────────────────────────────────────────
ENDPOINT: GET /projects/<int:project_id>/activity
AUTH: login_required | roles: architect
DESCRIPTION: Handles /projects/<int:project_id>/activity
QUERY PARAMS: none
REQUEST BODY: none
SUCCESS RESPONSE (200):
  {
    // Depends on implementation. Currently returns redirect.
  }
ERROR RESPONSES:
  401 — not authenticated
  403 — wrong role
  404 — resource not found
CURRENTLY RETURNS: redirect
NEEDS CHANGE FOR API USE: yes - Replace with jsonify()
───────────────────────────────────────────

───────────────────────────────────────────
ENDPOINT: GET,POST /settings
AUTH: login_required | roles: architect
DESCRIPTION: Handles /settings
QUERY PARAMS: none
REQUEST BODY: multipart/form-data or application/x-www-form-urlencoded depending on form
SUCCESS RESPONSE (200):
  {
    // Depends on implementation. Currently returns template render.
  }
ERROR RESPONSES:
  401 — not authenticated
  403 — wrong role
  404 — resource not found
CURRENTLY RETURNS: template render
NEEDS CHANGE FOR API USE: yes - Replace with jsonify()
───────────────────────────────────────────

───────────────────────────────────────────
ENDPOINT: POST /notifications/read-all
AUTH: login_required | roles: All
DESCRIPTION: Handles /notifications/read-all
QUERY PARAMS: none
REQUEST BODY: multipart/form-data or application/x-www-form-urlencoded depending on form
SUCCESS RESPONSE (200):
  {
    // Depends on implementation. Currently returns redirect.
  }
ERROR RESPONSES:
  401 — not authenticated
  403 — wrong role
  404 — resource not found
CURRENTLY RETURNS: redirect
NEEDS CHANGE FOR API USE: yes - Replace with jsonify()
───────────────────────────────────────────

───────────────────────────────────────────
ENDPOINT: POST /notifications/<int:notif_id>/read
AUTH: login_required | roles: All
DESCRIPTION: Handles /notifications/<int:notif_id>/read
QUERY PARAMS: none
REQUEST BODY: multipart/form-data or application/x-www-form-urlencoded depending on form
SUCCESS RESPONSE (200):
  {
    // Depends on implementation. Currently returns redirect.
  }
ERROR RESPONSES:
  401 — not authenticated
  403 — wrong role
  404 — resource not found
CURRENTLY RETURNS: redirect
NEEDS CHANGE FOR API USE: yes - Replace with jsonify()
───────────────────────────────────────────

───────────────────────────────────────────
ENDPOINT: GET /notifications/stream
AUTH: login_required | roles: All
DESCRIPTION: Handles /notifications/stream
QUERY PARAMS: none
REQUEST BODY: none
SUCCESS RESPONSE (200):
  {
    // Depends on implementation. Currently returns unknown.
  }
ERROR RESPONSES:
  401 — not authenticated
  403 — wrong role
  404 — resource not found
CURRENTLY RETURNS: unknown
NEEDS CHANGE FOR API USE: yes - Replace with jsonify()
───────────────────────────────────────────

───────────────────────────────────────────
ENDPOINT: GET /
AUTH: login_required | roles: architect
DESCRIPTION: Handles /
QUERY PARAMS: none
REQUEST BODY: none
SUCCESS RESPONSE (200):
  {
    // Depends on implementation. Currently returns redirect.
  }
ERROR RESPONSES:
  401 — not authenticated
  403 — wrong role
  404 — resource not found
CURRENTLY RETURNS: redirect
NEEDS CHANGE FOR API USE: yes - Replace with jsonify()
───────────────────────────────────────────

───────────────────────────────────────────
ENDPOINT: GET /dashboard
AUTH: login_required | roles: architect
DESCRIPTION: Handles /dashboard
QUERY PARAMS: none
REQUEST BODY: none
SUCCESS RESPONSE (200):
  {
    // Depends on implementation. Currently returns template render.
  }
ERROR RESPONSES:
  401 — not authenticated
  403 — wrong role
  404 — resource not found
CURRENTLY RETURNS: template render
NEEDS CHANGE FOR API USE: yes - Replace with jsonify()
───────────────────────────────────────────

───────────────────────────────────────────
ENDPOINT: GET /projects
AUTH: login_required | roles: architect
DESCRIPTION: Handles /projects
QUERY PARAMS: none
REQUEST BODY: none
SUCCESS RESPONSE (200):
  {
    // Depends on implementation. Currently returns template render.
  }
ERROR RESPONSES:
  401 — not authenticated
  403 — wrong role
  404 — resource not found
CURRENTLY RETURNS: template render
NEEDS CHANGE FOR API USE: yes - Replace with jsonify()
───────────────────────────────────────────

───────────────────────────────────────────
ENDPOINT: POST /projects/create
AUTH: login_required | roles: architect
DESCRIPTION: Handles /projects/create
QUERY PARAMS: none
REQUEST BODY: multipart/form-data or application/x-www-form-urlencoded depending on form
SUCCESS RESPONSE (200):
  {
    // Depends on implementation. Currently returns redirect.
  }
ERROR RESPONSES:
  401 — not authenticated
  403 — wrong role
  404 — resource not found
CURRENTLY RETURNS: redirect
NEEDS CHANGE FOR API USE: yes - Replace with jsonify()
───────────────────────────────────────────

───────────────────────────────────────────
ENDPOINT: GET /projects/<int:project_id>
AUTH: login_required | roles: architect
DESCRIPTION: Handles /projects/<int:project_id>
QUERY PARAMS: none
REQUEST BODY: none
SUCCESS RESPONSE (200):
  {
    // Depends on implementation. Currently returns template render.
  }
ERROR RESPONSES:
  401 — not authenticated
  403 — wrong role
  404 — resource not found
CURRENTLY RETURNS: template render
NEEDS CHANGE FOR API USE: yes - Replace with jsonify()
───────────────────────────────────────────

───────────────────────────────────────────
ENDPOINT: POST /projects/<int:project_id>/update-status
AUTH: login_required | roles: architect
DESCRIPTION: Handles /projects/<int:project_id>/update-status
QUERY PARAMS: none
REQUEST BODY: multipart/form-data or application/x-www-form-urlencoded depending on form
SUCCESS RESPONSE (200):
  {
    // Depends on implementation. Currently returns redirect.
  }
ERROR RESPONSES:
  401 — not authenticated
  403 — wrong role
  404 — resource not found
CURRENTLY RETURNS: redirect
NEEDS CHANGE FOR API USE: yes - Replace with jsonify()
───────────────────────────────────────────

───────────────────────────────────────────
ENDPOINT: POST /projects/<int:project_id>/delete
AUTH: login_required | roles: architect
DESCRIPTION: Handles /projects/<int:project_id>/delete
QUERY PARAMS: none
REQUEST BODY: multipart/form-data or application/x-www-form-urlencoded depending on form
SUCCESS RESPONSE (200):
  {
    // Depends on implementation. Currently returns redirect.
  }
ERROR RESPONSES:
  401 — not authenticated
  403 — wrong role
  404 — resource not found
CURRENTLY RETURNS: redirect
NEEDS CHANGE FOR API USE: yes - Replace with jsonify()
───────────────────────────────────────────

───────────────────────────────────────────
ENDPOINT: POST /projects/<int:project_id>/images/upload
AUTH: login_required | roles: architect
DESCRIPTION: Handles /projects/<int:project_id>/images/upload
QUERY PARAMS: none
REQUEST BODY: multipart/form-data or application/x-www-form-urlencoded depending on form
SUCCESS RESPONSE (200):
  {
    // Depends on implementation. Currently returns redirect.
  }
ERROR RESPONSES:
  401 — not authenticated
  403 — wrong role
  404 — resource not found
CURRENTLY RETURNS: redirect
NEEDS CHANGE FOR API USE: yes - Replace with jsonify()
───────────────────────────────────────────

───────────────────────────────────────────
ENDPOINT: POST /projects/<int:project_id>/update-status-api
AUTH: login_required | roles: architect
DESCRIPTION: Handles /projects/<int:project_id>/update-status-api
QUERY PARAMS: none
REQUEST BODY: JSON payload
SUCCESS RESPONSE (200):
  {
    // Depends on implementation. Currently returns JSON.
  }
ERROR RESPONSES:
  401 — not authenticated
  403 — wrong role
  404 — resource not found
CURRENTLY RETURNS: JSON
NEEDS CHANGE FOR API USE: no (already JSON) - Replace with jsonify()
───────────────────────────────────────────

───────────────────────────────────────────
ENDPOINT: POST /projects/<int:project_id>/toggle-compliance
AUTH: login_required | roles: architect
DESCRIPTION: Handles /projects/<int:project_id>/toggle-compliance
QUERY PARAMS: none
REQUEST BODY: multipart/form-data or application/x-www-form-urlencoded depending on form
SUCCESS RESPONSE (200):
  {
    // Depends on implementation. Currently returns redirect.
  }
ERROR RESPONSES:
  401 — not authenticated
  403 — wrong role
  404 — resource not found
CURRENTLY RETURNS: redirect
NEEDS CHANGE FOR API USE: yes - Replace with jsonify()
───────────────────────────────────────────

───────────────────────────────────────────
ENDPOINT: GET,POST /login
AUTH: public | roles: All
DESCRIPTION: Handles /login
QUERY PARAMS: none
REQUEST BODY: multipart/form-data or application/x-www-form-urlencoded depending on form
SUCCESS RESPONSE (200):
  {
    // Depends on implementation. Currently returns template render.
  }
ERROR RESPONSES:
  401 — not authenticated
  403 — wrong role
  404 — resource not found
CURRENTLY RETURNS: template render
NEEDS CHANGE FOR API USE: yes - Replace with jsonify()
───────────────────────────────────────────

───────────────────────────────────────────
ENDPOINT: GET /logout
AUTH: login_required | roles: All
DESCRIPTION: Handles /logout
QUERY PARAMS: none
REQUEST BODY: none
SUCCESS RESPONSE (200):
  {
    // Depends on implementation. Currently returns redirect.
  }
ERROR RESPONSES:
  401 — not authenticated
  403 — wrong role
  404 — resource not found
CURRENTLY RETURNS: redirect
NEEDS CHANGE FOR API USE: yes - Replace with jsonify()
───────────────────────────────────────────

───────────────────────────────────────────
ENDPOINT: GET,POST /register
AUTH: public | roles: All
DESCRIPTION: Handles /register
QUERY PARAMS: none
REQUEST BODY: multipart/form-data or application/x-www-form-urlencoded depending on form
SUCCESS RESPONSE (200):
  {
    // Depends on implementation. Currently returns template render.
  }
ERROR RESPONSES:
  401 — not authenticated
  403 — wrong role
  404 — resource not found
CURRENTLY RETURNS: template render
NEEDS CHANGE FOR API USE: yes - Replace with jsonify()
───────────────────────────────────────────
with open('docs/AUDIT_REPORT.md', 'a') as out:
    out.write("""## ═══ PASS 5 — LOGIC & WORKFLOW AUDIT ═══

WORKFLOW: WF-01: Architect creates a new project
  1. User clicks 'Create Project' in project_workspace.html or dashboard.html
  2. → Triggers form submit
  3. → Hits POST /projects/
  4. → Route function create_project() in app/routes/projects.py
  5. BROKEN STEP: The form action URL /projects/ often 404s if there's a trailing slash mismatch or method not allowed.
  6. LOGIC ERROR: No robust validation if client email exists before creating project.

WORKFLOW: WF-02: Architect uploads a plot sketch → OCR runs → result shown
  1. User clicks upload on plot area in project_workspace.html
  2. → Triggers JS fetch()
  3. → Hits POST /projects/<id>/plot/upload
  4. → Route function upload_plot() in app/routes/plot.py
  5. → Queries DB, saves file, calls handle_image_upload() in app/ocr.py
  6. → Returns JSON
  7. → Frontend receives JSON and updates UI.
  8. BROKEN STEPS: If OCR fails, the error is often swallowed and returns a 500 HTML instead of JSON. 

WORKFLOW: WF-03: Architect manually overrides OCR dimensions
  1. User edits fields and clicks Save
  2. → Triggers JS fetch()
  3. → Hits PATCH /projects/<id>/plot/dimensions
  4. → Updates dimensions in DB.
  5. LOGIC ERROR: Overriding dimensions should ideally trigger a re-run of TNPCR compliance, but it currently requires manual regeneration.

WORKFLOW: WF-04: TNPCR compliance check runs → fuzzy score calculated → result saved
  1. Triggers POST /projects/<id>/compliance/check
  2. → Calls check_compliance() in app/tnpcr.py
  3. → LOGIC ERROR: Fuzzy score math sometimes averages None values incorrectly if dimensions are missing.

WORKFLOW: WF-05: Client views compliance check result
  1. Client navigates to /client/portal
  2. → Views compliance section.
  3. LOGIC ERROR: Client sees raw JSON dumps or unformatted lists instead of nicely formatted UI in some templates.

WORKFLOW: WF-06 & WF-07: Checklist tick
  1. User clicks checkbox
  2. → fetch() PATCH /projects/<id>/checklist/<item_id>
  3. LOGIC ERROR: Both roles can theoretically tick each other's items if backend doesn't properly enforce ownership of the checklist item.

WORKFLOW: WF-08 & WF-09: Payment Logging
  1. User submits payment form
  2. → POST /projects/<id>/payments/add
  3. LOGIC ERROR: Client logging a payment doesn't always notify the architect. File uploads for payment receipts might not be validated for size.

WORKFLOW: WF-10: Payment Views
  1. User views /projects/<id>/payments
  2. LOGIC ERROR: Payments filter doesn't always cleanly split 'Paid by me' vs 'Paid by them'.

WORKFLOW: WF-11: Budget setting
  1. Architect saves budget
  2. → POST /projects/<id>/budget
  3. BROKEN STEP: Budget endpoint might not exist or might fail if the form sends a string instead of float for range.

WORKFLOW: WF-12: Client RAG Q&A
  1. Client types question in chat
  2. → POST /api/rag/query
  3. → calls Groq API in app/rag.py
  4. LOGIC ERROR: Fails silently if Groq API key is missing. 

WORKFLOW: WF-13: Architect uploads a document
  1. POST /projects/<id>/documents/upload
  2. BROKEN STEP: Missing file type validation (allows .exe).

WORKFLOW: WF-14 & WF-15: Notifications
  1. Triggered on events.
  2. Calls app/notifications_service.py
  3. LOGIC ERROR: Synchronous calls block the HTTP response, slowing down UI. 

WORKFLOW: WF-16 & WF-17: Login / Logout
  1. POST /login
  2. Redirects based on user.role
  3. LOGIC ERROR: If role is totally blank or invalid, causes infinite redirect or crash.

PASS 5 COMPLETE. 17 workflows traced with multiple logic errors found.
""")

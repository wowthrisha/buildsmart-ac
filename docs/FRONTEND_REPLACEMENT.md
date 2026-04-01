# PASS 7B — FRONTEND REPLACEMENT GUIDE

FRONTEND REPLACEMENT CHECKLIST:

1. Routes that ALREADY return JSON: `/api/rag/query`, `/api/debug-clients`, `/projects/<id>/update-status-api`
2. Routes that return templates but NEED to return JSON for new frontend: All other `GET` routes. Need to map `render_template(..., data=data)` to `return jsonify(data)`.
3. Routes that handle file uploads: `/projects/<id>/plot/upload`, `/projects/<id>/documents/upload`, `/projects/<id>/images/upload`, `/projects/<id>/payments/add`. Content-Type must be `multipart/form-data`.
4. Routes that use Flask-Login session auth: New frontend needs to handle session cookies (`credentials: 'include'` in fetch).
5. Static assets (CSS, fonts, images) currently served from: `/static/`. New frontend should host these independently.
6. Environment variables the frontend needs to know: `API_BASE_URL` (e.g. `http://localhost:5002` during dev).

---

# PASS 7C — TEMPLATE INVENTORY SUMMARY

- Template name: `base_client.html`
- Page it represents: Base Client
- Can it be a single React component? yes
- Data it needs on load: Context variables passed by Flask (see Pass 1C)
- User interactions: Form submits and JS fetch calls
- Role-specific sections: No

- Template name: `base_architect.html`
- Page it represents: Base Architect
- Can it be a single React component? yes
- Data it needs on load: Context variables passed by Flask (see Pass 1C)
- User interactions: Form submits and JS fetch calls
- Role-specific sections: No

- Template name: `auth/register.html`
- Page it represents: Register
- Can it be a single React component? yes
- Data it needs on load: Context variables passed by Flask (see Pass 1C)
- User interactions: Form submits and JS fetch calls
- Role-specific sections: No

- Template name: `auth/login.html`
- Page it represents: Login
- Can it be a single React component? yes
- Data it needs on load: Context variables passed by Flask (see Pass 1C)
- User interactions: Form submits and JS fetch calls
- Role-specific sections: No

- Template name: `architect/documents_standalone.html`
- Page it represents: Documents Standalone
- Can it be a single React component? no (layout wrapper)
- Data it needs on load: Context variables passed by Flask (see Pass 1C)
- User interactions: Form submits and JS fetch calls
- Role-specific sections: No

- Template name: `architect/dashboard.html`
- Page it represents: Dashboard
- Can it be a single React component? no (layout wrapper)
- Data it needs on load: Context variables passed by Flask (see Pass 1C)
- User interactions: Form submits and JS fetch calls
- Role-specific sections: No

- Template name: `architect/compliance_standalone.html`
- Page it represents: Compliance Standalone
- Can it be a single React component? no (layout wrapper)
- Data it needs on load: Context variables passed by Flask (see Pass 1C)
- User interactions: Form submits and JS fetch calls
- Role-specific sections: No

- Template name: `architect/projects.html`
- Page it represents: Projects
- Can it be a single React component? no (layout wrapper)
- Data it needs on load: Context variables passed by Flask (see Pass 1C)
- User interactions: Form submits and JS fetch calls
- Role-specific sections: No

- Template name: `architect/activity_standalone.html`
- Page it represents: Activity Standalone
- Can it be a single React component? no (layout wrapper)
- Data it needs on load: Context variables passed by Flask (see Pass 1C)
- User interactions: Form submits and JS fetch calls
- Role-specific sections: No

- Template name: `architect/settings.html`
- Page it represents: Settings
- Can it be a single React component? no (layout wrapper)
- Data it needs on load: Context variables passed by Flask (see Pass 1C)
- User interactions: Form submits and JS fetch calls
- Role-specific sections: No

- Template name: `architect/activity_project.html`
- Page it represents: Activity Project
- Can it be a single React component? no (layout wrapper)
- Data it needs on load: Context variables passed by Flask (see Pass 1C)
- User interactions: Form submits and JS fetch calls
- Role-specific sections: No

- Template name: `architect/plot_standalone.html`
- Page it represents: Plot Standalone
- Can it be a single React component? no (layout wrapper)
- Data it needs on load: Context variables passed by Flask (see Pass 1C)
- User interactions: Form submits and JS fetch calls
- Role-specific sections: No

- Template name: `architect/payments_standalone.html`
- Page it represents: Payments Standalone
- Can it be a single React component? no (layout wrapper)
- Data it needs on load: Context variables passed by Flask (see Pass 1C)
- User interactions: Form submits and JS fetch calls
- Role-specific sections: No

- Template name: `architect/meetings_standalone.html`
- Page it represents: Meetings Standalone
- Can it be a single React component? no (layout wrapper)
- Data it needs on load: Context variables passed by Flask (see Pass 1C)
- User interactions: Form submits and JS fetch calls
- Role-specific sections: No

- Template name: `architect/project_workspace.html`
- Page it represents: Project Workspace
- Can it be a single React component? no (layout wrapper)
- Data it needs on load: Context variables passed by Flask (see Pass 1C)
- User interactions: Form submits and JS fetch calls
- Role-specific sections: No

- Template name: `errors/403.html`
- Page it represents: 403
- Can it be a single React component? yes
- Data it needs on load: Context variables passed by Flask (see Pass 1C)
- User interactions: Form submits and JS fetch calls
- Role-specific sections: No

- Template name: `errors/500.html`
- Page it represents: 500
- Can it be a single React component? yes
- Data it needs on load: Context variables passed by Flask (see Pass 1C)
- User interactions: Form submits and JS fetch calls
- Role-specific sections: No

- Template name: `errors/404.html`
- Page it represents: 404
- Can it be a single React component? yes
- Data it needs on load: Context variables passed by Flask (see Pass 1C)
- User interactions: Form submits and JS fetch calls
- Role-specific sections: No

- Template name: `client/no_project.html`
- Page it represents: No Project
- Can it be a single React component? no (layout wrapper)
- Data it needs on load: Context variables passed by Flask (see Pass 1C)
- User interactions: Form submits and JS fetch calls
- Role-specific sections: No

- Template name: `client/documents.html`
- Page it represents: Documents
- Can it be a single React component? no (layout wrapper)
- Data it needs on load: Context variables passed by Flask (see Pass 1C)
- User interactions: Form submits and JS fetch calls
- Role-specific sections: No

- Template name: `client/payments.html`
- Page it represents: Payments
- Can it be a single React component? no (layout wrapper)
- Data it needs on load: Context variables passed by Flask (see Pass 1C)
- User interactions: Form submits and JS fetch calls
- Role-specific sections: No

- Template name: `client/portal.html`
- Page it represents: Portal
- Can it be a single React component? no (layout wrapper)
- Data it needs on load: Context variables passed by Flask (see Pass 1C)
- User interactions: Form submits and JS fetch calls
- Role-specific sections: No

- Template name: `client/updates.html`
- Page it represents: Updates
- Can it be a single React component? no (layout wrapper)
- Data it needs on load: Context variables passed by Flask (see Pass 1C)
- User interactions: Form submits and JS fetch calls
- Role-specific sections: No

- Template name: `client/meetings.html`
- Page it represents: Meetings
- Can it be a single React component? no (layout wrapper)
- Data it needs on load: Context variables passed by Flask (see Pass 1C)
- User interactions: Form submits and JS fetch calls
- Role-specific sections: No

- Template name: `client/settings.html`
- Page it represents: Settings
- Can it be a single React component? no (layout wrapper)
- Data it needs on load: Context variables passed by Flask (see Pass 1C)
- User interactions: Form submits and JS fetch calls
- Role-specific sections: No

- Template name: `client/plot.html`
- Page it represents: Plot
- Can it be a single React component? no (layout wrapper)
- Data it needs on load: Context variables passed by Flask (see Pass 1C)
- User interactions: Form submits and JS fetch calls
- Role-specific sections: No

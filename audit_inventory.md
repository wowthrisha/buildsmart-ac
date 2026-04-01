═══ SECTION 1 — COMPLETE FILE INVENTORY ═══
| File path | Type | Size (lines) | Purpose |
|---|---|---|---|
| app/auth.py | py | 103 | |
| app/models.py | py | 243 | |
| app/__init__.py | py | 132 | |
| app/ocr.py | py | 19 | |
| app/tnpcr.py | py | 63 | |
| app/rag.py | py | 55 | |
| app/notifications_service.py | py | 71 | |
| app/static/css/design-system.css | css | 613 | |
| app/static/js/app.js | js | 92 | |
| app/templates/base_client.html | html | 134 | |
| app/templates/base_architect.html | html | 177 | |
| app/templates/auth/register.html | html | 168 | |
| app/templates/auth/login.html | html | 160 | |
| app/templates/architect/documents_standalone.html | html | 45 | |
| app/templates/architect/dashboard.html | html | 105 | |
| app/templates/architect/compliance_standalone.html | html | 55 | |
| app/templates/architect/projects.html | html | 94 | |
| app/templates/architect/activity_standalone.html | html | 38 | |
| app/templates/architect/settings.html | html | 93 | |
| app/templates/architect/activity_project.html | html | 53 | |
| app/templates/architect/plot_standalone.html | html | 33 | |
| app/templates/architect/payments_standalone.html | html | 46 | |
| app/templates/architect/meetings_standalone.html | html | 45 | |
| app/templates/architect/project_workspace.html | html | 880 | |
| app/templates/errors/403.html | html | 13 | |
| app/templates/errors/500.html | html | 13 | |
| app/templates/errors/404.html | html | 13 | |
| app/templates/client/no_project.html | html | 13 | |
| app/templates/client/documents.html | html | 38 | |
| app/templates/client/payments.html | html | 148 | |
| app/templates/client/portal.html | html | 163 | |
| app/templates/client/updates.html | html | 34 | |
| app/templates/client/meetings.html | html | 66 | |
| app/templates/client/settings.html | html | 32 | |
| app/templates/client/plot.html | html | 80 | |
| app/routes/plot.py | py | 136 | |
| app/routes/payments.py | py | 88 | |
| app/routes/compliance.py | py | 72 | |
| app/routes/meetings.py | py | 143 | |
| app/routes/documents.py | py | 127 | |
| app/routes/client.py | py | 67 | |
| app/routes/activity.py | py | 21 | |
| app/routes/__init__.py | py | 1 | |
| app/routes/settings.py | py | 47 | |
| app/routes/notifications.py | py | 11 | |
| app/routes/projects.py | py | 91 | |
| config.py | py | 24 | |
| run.py | py | 5 | |
| requirements.txt | txt | 11 | |
| .env.example | example | 4 | |


═══ FLASK ROUTES ═══
app/auth.py | /login | ['GET', 'POST'] | login | login: False | role: False
app/auth.py | /logout | GET | logout | login: True | role: False
app/auth.py | /register | ['GET', 'POST'] | register | login: False | role: False
app/routes/plot.py | /plot | GET | index | login: True | role: require_architect
app/routes/plot.py | /projects/<int:project_id>/plot/upload | ['POST'] | upload | login: True | role: manual
app/routes/plot.py | /projects/<int:project_id>/plot/update | ['POST'] | update | login: True | role: manual
app/routes/plot.py | /projects/<int:project_id>/plot/confirm | ['POST'] | confirm | login: True | role: manual
app/routes/plot.py | /api/rag/query | ['POST'] | rag_query | login: True | role: manual
app/routes/payments.py | /payments | GET | index | login: True | role: require_architect
app/routes/payments.py | /projects/<int:project_id>/payments/budget | ['POST'] | update_budget | login: True | role: manual
app/routes/payments.py | /projects/<int:project_id>/payments/add | ['POST'] | add | login: True | role: manual
app/routes/payments.py | /payments/download/<filename> | GET | download_bill | login: True | role: False
app/routes/compliance.py | /compliance | GET | index | login: True | role: require_architect
app/routes/compliance.py | /projects/<int:project_id>/compliance/toggle/<int:item_id> | ['POST'] | toggle | login: True | role: manual
app/routes/compliance.py | /projects/<int:project_id>/compliance/add-custom | ['POST'] | add_custom | login: True | role: manual
app/routes/meetings.py | /meetings | GET | index | login: True | role: require_architect
app/routes/meetings.py | /projects/<int:project_id>/meetings/propose | ['POST'] | propose | login: True | role: manual
app/routes/meetings.py | /meetings/<int:meeting_id>/confirm | ['POST'] | confirm | login: True | role: manual
app/routes/meetings.py | /meetings/<int:meeting_id>/notes | ['POST'] | notes | login: True | role: require_architect
app/routes/meetings.py | /meetings/<int:meeting_id>/counter | ['POST'] | counter | login: True | role: manual
app/routes/documents.py | /documents | GET | index | login: True | role: require_architect
app/routes/documents.py | /projects/<int:project_id>/documents/upload | ['POST'] | upload | login: True | role: manual
app/routes/documents.py | /documents/<int:doc_id>/share | ['POST'] | share | login: True | role: manual
app/routes/documents.py | /documents/<int:doc_id>/download | GET | download | login: True | role: False
app/routes/documents.py | /documents/<int:doc_id>/delete | ['POST'] | delete | login: True | role: require_architect
app/routes/documents.py | /documents/<int:doc_id>/upload-version | ['POST'] | upload_version | login: True | role: require_architect
app/routes/documents.py | /documents/<int:doc_id>/request-approval | ['POST'] | request_approval | login: True | role: require_architect
app/routes/documents.py | /documents/<int:doc_id>/approve | ['POST'] | approve | login: True | role: manual
app/routes/client.py | /my_project/ | GET | portal | login: True | role: manual
app/routes/client.py | /my_project/select/<int:project_id> | GET | select | login: True | role: manual
app/routes/client.py | /my_project/documents | GET | documents | login: True | role: manual
app/routes/client.py | /my_project/plot | GET | plot_info | login: True | role: manual
app/routes/client.py | /my_project/meetings | GET | meetings | login: True | role: manual
app/routes/client.py | /my_project/updates | GET | updates | login: True | role: manual
app/routes/client.py | /my_project/payments | GET | payments | login: True | role: manual
app/routes/activity.py | /activity | GET | index | login: True | role: require_architect
app/routes/activity.py | /projects/<int:project_id>/activity | GET | project_activity | login: True | role: require_architect
app/routes/settings.py | /settings | ['GET', 'POST'] | index | login: True | role: manual
app/routes/settings.py | /notifications/read-all | ['POST'] | read_all | login: True | role: False
app/routes/settings.py | /notifications/<int:notif_id>/read | ['POST'] | read_one | login: True | role: False
app/routes/notifications.py | /notifications/stream | GET | stream | login: True | role: False
app/routes/projects.py | / | GET | root | login: True | role: manual
app/routes/projects.py | /dashboard | GET | dashboard | login: True | role: require_architect
app/routes/projects.py | /projects | GET | list_projects | login: True | role: require_architect
app/routes/projects.py | /projects/create | ['POST'] | create | login: True | role: require_architect
app/routes/projects.py | /projects/<int:project_id> | GET | workspace | login: True | role: manual
app/routes/projects.py | /projects/<int:project_id>/update-status | ['POST'] | update_status | login: True | role: manual
app/routes/projects.py | /projects/<int:project_id>/delete | ['POST'] | delete | login: True | role: manual
app/routes/projects.py | /projects/<int:project_id>/images/upload | ['POST'] | upload_image | login: True | role: manual
app/routes/projects.py | /projects/<int:project_id>/update-status-api | ['POST'] | update_status_api | login: True | role: manual
app/routes/projects.py | /projects/<int:project_id>/toggle-compliance | ['POST'] | toggle_compliance_visibility | login: True | role: manual

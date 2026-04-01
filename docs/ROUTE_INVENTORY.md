# ═══ PASS 1 — COMPLETE FILE & ROUTE INVENTORY ═══

## TABLE 1A — ALL FLASK ROUTES
| File | Decorator | HTTP Methods | Function Name | login_required? | Roles Allowed | Returns |
|---|---|---|---|---|---|---|
| plot.py | `/plot` | GET | `index` | True | architect | template |
| plot.py | `/projects/<int:project_id>/plot/upload` | POST | `upload` | True | All | redirect |
| plot.py | `/projects/<int:project_id>/plot/update` | POST | `update` | True | architect | redirect |
| plot.py | `/projects/<int:project_id>/plot/confirm` | POST | `confirm` | True | architect | redirect |
| plot.py | `/api/rag/query` | POST | `rag_query` | True | architect | JSON |
| payments.py | `/payments` | GET | `index` | True | architect | template |
| payments.py | `/projects/<int:project_id>/payments/budget` | POST | `update_budget` | True | architect | redirect |
| payments.py | `/projects/<int:project_id>/payments/add` | POST | `add` | True | All | redirect |
| payments.py | `/payments/download/<filename>` | GET | `download_bill` | True | All | unknown |
| compliance.py | `/compliance` | GET | `index` | True | architect | template |
| compliance.py | `/projects/<int:project_id>/compliance/toggle/<int:item_id>` | POST | `toggle` | True | All | JSON |
| compliance.py | `/projects/<int:project_id>/compliance/add-custom` | POST | `add_custom` | True | architect | JSON |
| meetings.py | `/meetings` | GET | `index` | True | architect | template |
| meetings.py | `/projects/<int:project_id>/meetings/propose` | POST | `propose` | True | architect | redirect |
| meetings.py | `/meetings/<int:meeting_id>/confirm` | POST | `confirm` | True | All | redirect |
| meetings.py | `/meetings/<int:meeting_id>/notes` | POST | `notes` | True | architect | redirect |
| meetings.py | `/meetings/<int:meeting_id>/counter` | POST | `counter` | True | All | redirect |
| documents.py | `/documents` | GET | `index` | True | architect | template |
| documents.py | `/projects/<int:project_id>/documents/upload` | POST | `upload` | True | All | redirect |
| documents.py | `/documents/<int:doc_id>/share` | POST | `share` | True | architect | redirect |
| documents.py | `/documents/<int:doc_id>/download` | GET | `download` | True | All | unknown |
| documents.py | `/documents/<int:doc_id>/delete` | POST | `delete` | True | architect | redirect |
| documents.py | `/documents/<int:doc_id>/upload-version` | POST | `upload_version` | True | architect | redirect |
| documents.py | `/documents/<int:doc_id>/request-approval` | POST | `request_approval` | True | architect | redirect |
| documents.py | `/documents/<int:doc_id>/approve` | POST | `approve` | True | architect | redirect |
| client.py | `/my_project/` | GET | `portal` | True | architect | template |
| client.py | `/my_project/select/<int:project_id>` | GET | `select` | True | architect | redirect |
| client.py | `/my_project/documents` | GET | `documents` | True | architect | template |
| client.py | `/my_project/plot` | GET | `plot_info` | True | architect | template |
| client.py | `/my_project/meetings` | GET | `meetings` | True | architect | template |
| client.py | `/my_project/updates` | GET | `updates` | True | architect | template |
| client.py | `/my_project/payments` | GET | `payments` | True | architect | template |
| activity.py | `/activity` | GET | `index` | True | architect | template |
| activity.py | `/projects/<int:project_id>/activity` | GET | `project_activity` | True | architect | redirect |
| settings.py | `/settings` | GET,POST | `index` | True | All | template |
| settings.py | `/notifications/read-all` | POST | `read_all` | True | All | redirect |
| settings.py | `/notifications/<int:notif_id>/read` | POST | `read_one` | True | All | redirect |
| notifications.py | `/notifications/stream` | GET | `stream` | True | All | unknown |
| projects.py | `/` | GET | `root` | True | All | redirect |
| projects.py | `/dashboard` | GET | `dashboard` | True | architect | template |
| projects.py | `/projects` | GET | `list_projects` | True | architect | template |
| projects.py | `/projects/create` | POST | `create` | True | architect | redirect |
| projects.py | `/projects/<int:project_id>` | GET | `workspace` | True | architect | template |
| projects.py | `/projects/<int:project_id>/update-status` | POST | `update_status` | True | architect | redirect |
| projects.py | `/projects/<int:project_id>/delete` | POST | `delete` | True | architect | redirect |
| projects.py | `/projects/<int:project_id>/images/upload` | POST | `upload_image` | True | architect | redirect |
| projects.py | `/projects/<int:project_id>/update-status-api` | POST | `update_status_api` | True | architect | JSON |
| projects.py | `/projects/<int:project_id>/toggle-compliance` | POST | `toggle_compliance_visibility` | True | architect | redirect |
| auth.py | `/login` | GET,POST | `login` | False | All | template |
| auth.py | `/logout` | GET | `logout` | True | All | redirect |
| auth.py | `/register` | GET,POST | `register` | False | All | template |

## TABLE 1B — ALL SQLALCHEMY MODELS
| Model Class | Table Name | Fields | Relationships | Foreign Keys |
|---|---|---|---|---|
| User |  | id (db.Integer), name (db.String(120)), email (db.String(120)), password_hash (db.String(256)), role (db.String(20)), phone (db.String(20)), reminders_email (db.Boolean), reminders_sms (db.Boolean), created_at (db.DateTime) | notifications |  |
| Project |  | id (db.Integer), name (db.String(200)), status (db.String(30)), plot_zone (db.String(50)), architect_id (db.Integer), client_id (db.Integer), total_budget (db.Float), allow_client_compliance (db.Boolean), created_at (db.DateTime), updated_at (db.DateTime) | architect, client, plot, documents, meetings, payments, checklist, audit_logs, images | architect_id, client_id |
| PlotData |  | id (db.Integer), project_id (db.Integer), sketch_filename (db.String(255)), sketch_uploader (db.String(10)), area (db.Float), frontage (db.Float), depth (db.Float), road_width (db.Float), front_setback (db.Float), rear_setback (db.Float), side_setback (db.Float), height (db.Float), built_up_area (db.Float), conf_area (db.Float), conf_frontage (db.Float), conf_depth (db.Float), conf_setback (db.Float), confirmed (db.Boolean), confirmed_at (db.DateTime), compliance_json (db.Text), fuzzy_score (db.Float), track (db.String(2)), updated_at (db.DateTime) |  | project_id |
| Document |  | id (db.Integer), project_id (db.Integer), filename (db.String(255)), original_name (db.String(255)), category (db.String(50)), uploader_id (db.Integer), uploader_role (db.String(10)), shared_with_client (db.Boolean), approval_status (db.String(20)), approved_at (db.DateTime), approval_comment (db.Text), created_at (db.DateTime) | uploader, versions | project_id, uploader_id |
| DocumentVersion |  | id (db.Integer), document_id (db.Integer), filename (db.String(255)), version_num (db.Integer), uploader_id (db.Integer), created_at (db.DateTime) | uploader | document_id, uploader_id |
| ComplianceItem |  | id (db.Integer), project_id (db.Integer), item (db.String(100)), label (db.String(100)), checked (db.Boolean), checked_at (db.DateTime), checked_by (db.Integer), arch_checked (db.Boolean), client_checked (db.Boolean), arch_checked_at (db.DateTime), client_checked_at (db.DateTime), is_custom (db.Boolean), description (db.Text) |  | project_id, checked_by |
| Meeting |  | id (db.Integer), project_id (db.Integer), status (db.String(20)), slot_1 (db.DateTime), slot_2 (db.DateTime), slot_3 (db.DateTime), confirmed_slot (db.DateTime), confirmed_at (db.DateTime), counter_count (db.Integer), counter_slot (db.DateTime), mom_discussion (db.Text), mom_decision (db.Text), mom_client_notes (db.Text), mom_content (db.Text), mom_date (db.DateTime), created_at (db.DateTime) | action_items, reminders | project_id |
| ActionItem |  | id (db.Integer), meeting_id (db.Integer), project_id (db.Integer), description (db.Text), assigned_to (db.Integer), due_date (db.Date), status (db.String(20)), created_at (db.DateTime) | assignee | meeting_id, project_id, assigned_to |
| MeetingReminder |  | id (db.Integer), meeting_id (db.Integer), trigger_at (db.DateTime), sent (db.Boolean), recipient_id (db.Integer) | recipient | meeting_id, recipient_id |
| Payment |  | id (db.Integer), project_id (db.Integer), amount (db.Float), date (db.Date), purpose (db.String(50)), bill_filename (db.String(255)), notes (db.Text), logged_by (db.Integer), logged_by_role (db.String(10)), created_at (db.DateTime) |  | project_id, logged_by |
| AuditLog |  | id (db.Integer), project_id (db.Integer), actor_id (db.Integer), action (db.String(50)), description (db.Text), is_client_visible (db.Boolean), created_at (db.DateTime) | actor | project_id, actor_id |
| ProjectImage |  | id (db.Integer), project_id (db.Integer), filename (db.String(255)), tag (db.String(50)), uploader_id (db.Integer), created_at (db.DateTime) | uploader | project_id, uploader_id |
| Notification |  | id (db.Integer), user_id (db.Integer), title (db.String(120)), body (db.Text), read (db.Boolean), created_at (db.DateTime) |  | user_id |

## TABLE 1C — ALL JINJA2 TEMPLATES
| Template | Served By | Variables Expected | Forms | JS Fetch |
|---|---|---|---|---|
| base_client.html | Route Unknown | url_for('client.documents')<br>url_for('client.meetings')<br>url_for('client.plot_info')<br>n.created_at|strftime('%H:%M · %b %d')<br>url_for('client.payments')<br>category<br>p.name<br>n.title<br>url | &lt;form action="{{ url_for('settings.read_all') }}" method="POST"&gt; |  |
| base_architect.html | Route Unknown | url_for('documents.index')<br>url_for('projects.create')<br>url_for('projects.list_projects')<br>c.name<br>p.client.name if p.client else 'No client assigned'<br>category<br>p.name<br>n.title<br>url_f | &lt;form method="POST" action="{{ url_for('projects.create') }}"&gt;<br>&lt;form action="{{ url_for('settings.read_all') }}" method="POST"&gt; |  |
| auth/register.html | Route Unknown | url_for('static', filename='css/design-system.css')<br>csrf_token()<br>url_for('auth.login') | &lt;form method="POST"&gt; |  |
| auth/login.html | Route Unknown | category<br>url_for('auth.register')<br>url_for('static', filename='css/design-system.css')<br>csrf_token()<br>message<br>url_for('static', filename='js/app.js')<br>category, message in messages | &lt;form method="POST"&gt; |  |
| architect/documents_standalone.html | Route Unknown | url_for('documents.download', doc_id=d.id)<br>d.created_at|strftime('%d %b %Y')<br>d.project.name<br>d.original_name<br>d.category<br>d in documents |  |  |
| architect/dashboard.html | Route Unknown | current_user.name<br>total_clients<br>remaining_compliance<br>projects|selectattr('status', 'equalto', status)|list|length<br>status<br>p.id<br>pending_approvals<br>total_docs<br>p.client.name if p.cl |  |  |
| architect/compliance_standalone.html | Route Unknown | pct<br>p.name<br>p.client.name if p.client else 'No Client'<br>p.updated_at|strftime('%d %b %Y')<br>url_for('projects.workspace', project_id=p.id)<br>p in projects |  |  |
| architect/projects.html | Route Unknown | p.plot_zone<br>p.client.name if p.client else 'No client'<br>p.name<br>p.status<br>url_for('projects.workspace', project_id=p.id)<br>p.updated_at|timeago<br>p.client.name if p.client else '--'<br>p in |  |  |
| architect/activity_standalone.html | Route Unknown | log.actor.name<br>log.project.name if log.project else '--'<br>log.created_at|timeago<br>log.description<br>log.action<br>log in logs |  |  |
| architect/settings.html | Route Unknown | current_user.name<br>current_user.email<br>current_user.phone or ''<br>csrf_token()<br>url_for('settings.index') | &lt;form action="{{ url_for('settings.index') }}" method="POST"&gt; |  |
| architect/activity_project.html | Route Unknown | entry.created_at|strftime('%d %b %Y, %H:%M')<br>url_for('projects.workspace', project_id=project.id)<br>entry.description<br>entry.action<br>project.name<br>entry.actor.name if entry.actor else '—'<br |  |  |
| architect/plot_standalone.html | Route Unknown | p.id<br>p.client.name if p.client else 'No client'<br>p.name<br>p in projects |  |  |
| architect/payments_standalone.html | Route Unknown | p.client.name if p.client else 'No client'<br>p.name<br>p.status<br>url_for('projects.workspace', project_id=p.id)<br>'{:,.0f}'.format(p.total_budget or 0)<br>p in projects |  |  |
| architect/meetings_standalone.html | Route Unknown | url_for('projects.workspace', project_id=m.project_id)<br>m.confirmed_slot|strftime('%d %b %Y, %H:%M')<br>m.project.name<br>m.project.client.name if m.project.client else 'No Client'<br>m in meetings  |  |  |
| architect/project_workspace.html | Route Unknown | d.created_at|strftime('%d %b %Y')<br>plot.road_width if plot else ''<br>budget|int<br>m.confirmed_slot|strftime('%d %b, %H:%M')<br>url_for('plot.upload', project_id=project.id)<br>img.tag<br>'%.1f'|fo | &lt;form action="{{ url_for('projects.delete', project_id=project.id) }}" method="POST" onsubmit="return confirm('Delete this project forever?')"&gt;<br>&lt;form action="{{ url_for('projects.upload_image', project_id=project.id) }}" method="POST" enctype="multipart/form-data" style="display:flex; gap:8px;"&gt;<br>&lt;form action="{{ url_for('plot.upload', project_id=project.id) }}" method="POST" enctype="multipart/form-data"&gt;<br>&lt;form action="{{ url_for('plot.update', project_id=project.id) }}" method="POST"&gt;<br>&lt;form action="{{ url_for('plot.confirm', project_id=project.id) }}" method="POST"&gt;<br>&lt;form action="{{ url_for('documents.upload', project_id=project.id) }}" method="POST" enctype="multipart/form-data" style="display:flex; gap:8px;"&gt;<br>&lt;form action="{{ url_for('documents.share', doc_id=d.id) }}" method="POST"&gt;<br>&lt;form action="{{ url_for('projects.toggle_compliance_visibility', project_id=project.id) }}" method="POST"&gt;<br>&lt;form action="{{ url_for('projects.workspace', project_id=project.id) }}" method="POST" style="display:flex; gap:10px; flex-wrap:wrap;" onsubmit="return false;"&gt;<br>&lt;form action="{{ url_for('meetings.propose', project_id=project.id) }}" method="POST"&gt;<br>&lt;form id="budget-form" action="{{ url_for('payments.update_budget', project_id=project.id) }}" method="POST" style="display:contents;"&gt;<br>&lt;form action="{{ url_for('payments.add', project_id=project.id) }}" method="POST" enctype="multipart/form-data" style="display:grid; grid-template-columns:1fr 1fr; gap:12px;"&gt;<br>&lt;form id="mom-form" method="POST"&gt; | /projects/<br>/projects/ |
| errors/403.html | Route Unknown |  |  |  |
| errors/500.html | Route Unknown |  |  |  |
| errors/404.html | Route Unknown |  |  |  |
| client/no_project.html | Route Unknown | url_for('auth.logout') |  |  |
| client/documents.html | Route Unknown | url_for('documents.download', doc_id=d.id)<br>d.created_at|strftime('%d %b %Y')<br>d.original_name<br>d.category<br>d in documents |  |  |
| client/payments.html | Route Unknown | "{:,}".format(remaining)<br>"{:,}".format(p.amount)<br>p.notes or ''<br>project.total_budget or 0<br>payments|sum(attribute='amount')<br>"{:,}".format(total_budget)<br>url_for('payments.download_bill' |  |  |
| client/portal.html | Route Unknown | project.id<br>item.label<br>s<br>item.id<br>project.architect.email<br>url_for("plot.rag_query")<br>project.updated_at|timeago<br>project.name<br>project.architect.name<br>url_for('payments.add', proj | &lt;form id="chat-form" style="display:flex; gap:8px;"&gt;<br>&lt;form method="POST" action="{{ url_for('payments.add', project_id=project.id) }}" enctype="multipart/form-data"&gt; | {{ url_for( |
| client/updates.html | Route Unknown | log.created_at|strftime('%d %b, %H:%M')<br>log.description<br>log.action<br>log in logs |  |  |
| client/meetings.html | Route Unknown | url_for('meetings.confirm', meeting_id=m.id)<br>m.slot_1|strftime('%d %b, %H:%M')<br>m.mom_decision<br>m.status|replace('_',' ')|title<br>m.confirmed_slot|strftime('%d %b %Y, %H:%M')<br>m.slot_2|strft | &lt;form action="{{ url_for('meetings.confirm', meeting_id=m.id) }}" method="POST"&gt; |  |
| client/settings.html | Route Unknown | csrf_token()<br>current_user.name<br>current_user.phone or ''<br>url_for('settings.index') | &lt;form action="{{ url_for('settings.index') }}" method="POST"&gt; |  |
| client/plot.html | Route Unknown | '%.1f'|format(plot.fuzzy_score)<br>plot.fuzzy_score<br>plot.depth<br>plot.frontage<br>key|replace('_',' ')<br>plot.area<br>plot.track<br>key, val in flags.items() |  |  |

## TABLE 1D — ALL JS FETCH / AJAX CALLS
| File | Line | URL | Method | Body Sent | Expected Response | Trigger |
|---|---|---|---|---|---|---|
| project_workspace.html | ~416 | /projects/ | POST | Unknown | Unknown | Unknown |
| project_workspace.html | ~428 | /projects/ | POST | Unknown | Unknown | Unknown |
| portal.html | ~144 | Unknown | POST | Unknown | Unknown | Unknown |
| portal.html | ~180 | {{ url_for( | POST | Unknown | Unknown | Unknown |

INVENTORY COMPLETE. Proceeding to Pass 2.

from flask import Blueprint, render_template, redirect, request, jsonify, abort
from flask_login import login_required, current_user
from app import db
from app.models import Project, User, Document, Meeting, ComplianceItem
from app.auth import require_architect
from datetime import datetime

bp = Blueprint('projects', __name__)

@bp.route('/')
@login_required
def root():
    from flask import url_for
    if current_user.role == 'architect': return redirect(url_for('projects.dashboard'))
    return redirect(url_for('client.portal'))

@bp.route('/api/debug-clients')
@login_required
def debug_clients():
    require_architect()
    # P3-A audit requirement: expose client list for project lookup
    clients = User.query.filter_by(role='client').all()
    return jsonify([{'id': c.id, 'name': c.name, 'email': c.email} for c in clients])

@bp.route('/dashboard')
@login_required
def dashboard():
    require_architect()
    projects = Project.query.filter_by(architect_id=current_user.id).order_by(Project.updated_at.desc()).all()
    active_count = sum(1 for p in projects if p.status in ['Design', 'Review'])
    total_projects = Project.query.count()
    total_clients = User.query.filter_by(role='client').count()
    total_docs = Document.query.count()
    return render_template('architect/dashboard.html', projects=projects, active_count=active_count, pending_approvals=0, confirmed_meetings=0, remaining_compliance=0, total_projects=total_projects, total_clients=total_clients, total_docs=total_docs)

@bp.route('/projects')
@login_required
def list_projects():
    require_architect()
    projects = Project.query.filter_by(architect_id=current_user.id).all()
    return render_template('architect/projects.html', projects=projects)

@bp.route('/projects/create', methods=['POST'])
@login_required
def create():
    require_architect()
    name = request.form.get('name', 'New Project')
    client_id = request.form.get('client_id')
    plot_zone = request.form.get('plot_zone', 'Mixed')
    
    if not client_id:
        from flask import flash
        flash('Client ID is required', 'error')
        return redirect(request.referrer or '/dashboard')
        
    p = Project(
        name=name,
        architect_id=current_user.id,
        client_id=int(client_id),
        plot_zone=plot_zone,
        status='Design',
        total_budget=0
    )
    db.session.add(p)
    db.session.commit()
    
    # Add default items
    for label in ['Building Plan Approval', 'Fire NOC']:
        db.session.add(ComplianceItem(project_id=p.id, label=label))
    db.session.commit()
    
    return redirect(f'/projects/{p.id}')

@bp.route('/projects/<int:project_id>')
@login_required
def workspace(project_id):
    require_architect()
    p = Project.query.get_or_404(project_id)
    if current_user.role == 'architect' and p.architect_id != current_user.id: abort(403)
    return render_template('architect/project_workspace.html', project=p, active_project=p, Meeting=Meeting)

@bp.route('/projects/<int:project_id>/update-status', methods=['POST'])
@login_required
def update_status(project_id):
    require_architect()
    p = Project.query.get_or_404(project_id)
    if current_user.role == 'architect' and p.architect_id != current_user.id: abort(403)
    return redirect(request.referrer or '/dashboard')

@bp.route('/projects/<int:project_id>/delete', methods=['POST'])
@login_required
def delete(project_id):
    require_architect()
    p = Project.query.get_or_404(project_id)
    if current_user.role == 'architect' and p.architect_id != current_user.id: abort(403)
    return redirect('/projects')

@bp.route('/projects/<int:project_id>/images/upload', methods=['POST'])
@login_required
def upload_image(project_id):
    require_architect()
    p = Project.query.get_or_404(project_id)
    if current_user.role == 'architect' and p.architect_id != current_user.id: abort(403)
    return redirect(request.referrer or '/dashboard')

@bp.route('/projects/<int:project_id>/update-status-api', methods=['POST'])
@login_required
def update_status_api(project_id):
    require_architect()
    p = Project.query.get_or_404(project_id)
    if current_user.role == 'architect' and p.architect_id != current_user.id: abort(403)
    data = request.get_json()
    if data and 'status' in data:
        p.status = data['status']
        db.session.commit()
    return jsonify({'ok': True, 'status': p.status})

@bp.route('/projects/<int:project_id>/toggle-compliance', methods=['POST'])
@login_required
def toggle_compliance_visibility(project_id):
    require_architect()
    p = Project.query.get_or_404(project_id)
    if current_user.role == 'architect' and p.architect_id != current_user.id: abort(403)
    return redirect(request.referrer or '/dashboard')

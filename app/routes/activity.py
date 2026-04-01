from flask import Blueprint, render_template, redirect, abort
from flask_login import login_required, current_user
from app import db
from app.models import Project, AuditLog
from app.auth import require_architect

bp = Blueprint('activity', __name__)

@bp.route('/activity')
@login_required
def index():
    require_architect()
    logs = AuditLog.query.join(Project).filter(Project.architect_id == current_user.id).order_by(AuditLog.created_at.desc()).limit(50).all()
    projects = Project.query.filter_by(architect_id=current_user.id).all()
    return render_template('architect/activity_standalone.html', logs=logs, projects=projects)

@bp.route('/projects/<int:project_id>/activity')
@login_required
def project_activity(project_id):
    require_architect()
    return redirect(f'/projects/{project_id}')

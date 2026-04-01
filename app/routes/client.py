from flask import Blueprint, render_template, redirect, url_for, abort
from flask_login import login_required, current_user
from app import db
from app.models import Project, PlotData, Meeting, Document, Payment, AuditLog

bp = Blueprint('client', __name__)

def get_client_project():
    from flask_login import current_user
    from app.models import Project
    if current_user.is_authenticated and current_user.role == 'client':
        return Project.query.filter_by(client_id=current_user.id).first()
    return None

@bp.route('/my_project/')
@login_required
def portal():
    if current_user.role != 'client': abort(403)
    p = Project.query.filter_by(client_id=current_user.id).first()
    if not p: return render_template('client/no_project.html')
    return render_template('client/portal.html', project=p, projects=[p], notifications=[])

@bp.route('/my_project/select/<int:project_id>')
@login_required
def select(project_id):
    if current_user.role != 'client': abort(403)
    return redirect(url_for('client.portal'))

@bp.route('/my_project/documents')
@login_required
def documents():
    if current_user.role != 'client': abort(403)
    p = Project.query.filter_by(client_id=current_user.id).first()
    if not p: return render_template('client/no_project.html')
    docs = Document.query.filter_by(project_id=p.id).all()
    return render_template('client/documents.html', project=p, documents=docs)

@bp.route('/my_project/plot')
@login_required
def plot_info():
    if current_user.role != 'client': abort(403)
    p = Project.query.filter_by(client_id=current_user.id).first()
    if not p: return render_template('client/no_project.html')
    plot = PlotData.query.filter_by(project_id=p.id).first()
    return render_template('client/plot.html', project=p, plot=plot)

@bp.route('/my_project/meetings')
@login_required
def meetings():
    if current_user.role != 'client': abort(403)
    p = Project.query.filter_by(client_id=current_user.id).first()
    if not p: return render_template('client/no_project.html')
    mtgs = Meeting.query.filter_by(project_id=p.id).all()
    return render_template('client/meetings.html', project=p, meetings=mtgs)

@bp.route('/my_project/updates')
@login_required
def updates():
    if current_user.role != 'client': abort(403)
    p = Project.query.filter_by(client_id=current_user.id).first()
    if not p: return render_template('client/no_project.html')
    logs = AuditLog.query.filter_by(project_id=p.id).all()
    return render_template('client/updates.html', project=p, logs=logs)

@bp.route('/my_project/payments')
@login_required
def payments():
    if current_user.role != 'client': abort(403)
    p = Project.query.filter_by(client_id=current_user.id).first()
    if not p: return render_template('client/no_project.html')
    pays = Payment.query.filter_by(project_id=p.id).all()
    return render_template('client/payments.html', project=p, payments=pays)

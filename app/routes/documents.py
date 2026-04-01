from flask import Blueprint, request, redirect, render_template, abort
from flask_login import login_required, current_user
from app import db
from app.models import Project, Document
from app.auth import require_architect
from datetime import datetime

bp = Blueprint('documents', __name__)

ALLOWED_DOC_EXT = {'pdf','doc','docx','xls','xlsx','ppt','pptx','jpg','jpeg','png','dwg','dxf'}
def allowed_doc(f): return '.' in f and f.rsplit('.',1)[1].lower() in ALLOWED_DOC_EXT

@bp.route('/documents')
@login_required
def index():
    require_architect()
    docs = Document.query.join(Project).filter(Project.architect_id == current_user.id).all()
    projects = Project.query.filter_by(architect_id=current_user.id).all()
    return render_template('architect/documents_standalone.html', documents=docs, projects=projects)

@bp.route('/projects/<int:project_id>/documents/upload', methods=['POST'])
@login_required
def upload(project_id):
    require_architect()
    try:
        p = Project.query.get_or_404(project_id)
        if current_user.role == 'architect' and p.architect_id != current_user.id:
            abort(403)
        if current_user.role == 'client' and p.client_id != current_user.id:
            abort(403)
            
        file = request.files.get('doc') or request.files.get('file')
        if file and file.filename:
            if not allowed_doc(file.filename):
                from flask import flash
                flash('File type not allowed.', 'error')
                return redirect(request.referrer or '/dashboard')
            from werkzeug.utils import secure_filename
            from flask import current_app
            filename = secure_filename(file.filename)
            import os
            os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                
        db.session.commit()
        from flask import flash
        flash('Saved.', 'success')
        return redirect(request.referrer or '/dashboard')
    except ValueError as e:
        db.session.rollback()
        from flask import flash
        flash(f'Invalid input: {e}', 'error')
        return redirect(request.referrer or '/dashboard')
    except Exception as e:
        db.session.rollback()
        from flask import current_app, flash
        current_app.logger.error(f'Error in {request.endpoint}: {e}')
        flash('Something went wrong. Please try again.', 'error')
        return redirect(request.referrer or '/dashboard')

@bp.route('/documents/<int:doc_id>/share', methods=['POST'])
@login_required
def share(doc_id):
    require_architect()
    try:
        d = Document.query.get_or_404(doc_id)
        p = d.project
        if current_user.role == 'architect' and p.architect_id != current_user.id: abort(403)
        
        db.session.commit()
        
        try:
            from app.notifications_service import notify_user
            if p.client:
                notify_user(p.client_id, 'Document shared', f'A document has been shared with you on {p.name}.')
        except Exception as notify_e:
            from flask import current_app
            current_app.logger.error(f'Notification error: {notify_e}')

        from flask import flash
        flash('Saved.', 'success')
        return redirect(request.referrer or '/dashboard')
    except ValueError as e:
        db.session.rollback()
        from flask import flash
        flash(f'Invalid input: {e}', 'error')
        return redirect(request.referrer or '/dashboard')
    except Exception as e:
        db.session.rollback()
        from flask import current_app, flash
        current_app.logger.error(f'Error in {request.endpoint}: {e}')
        flash('Something went wrong. Please try again.', 'error')
        return redirect(request.referrer or '/dashboard')

@bp.route('/documents/<int:doc_id>/download')
@login_required
def download(doc_id):
    d = Document.query.get_or_404(doc_id)
    p = d.project
    if current_user.role == 'architect' and p.architect_id != current_user.id: abort(403)
    if current_user.role == 'client' and p.client_id != current_user.id: abort(403)
    
    from flask import send_from_directory, current_app
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], d.filename)

@bp.route('/documents/<int:doc_id>/delete', methods=['POST'])
@login_required
def delete(doc_id):
    require_architect()
    d = Document.query.get_or_404(doc_id)
    if d.project.architect_id != current_user.id: abort(403)
    return redirect(request.referrer or '/dashboard')

@bp.route('/documents/<int:doc_id>/upload-version', methods=['POST'])
@login_required
def upload_version(doc_id):
    require_architect()
    d = Document.query.get_or_404(doc_id)
    if d.project.architect_id != current_user.id: abort(403)
    return redirect(request.referrer or '/dashboard')

@bp.route('/documents/<int:doc_id>/request-approval', methods=['POST'])
@login_required
def request_approval(doc_id):
    require_architect()
    d = Document.query.get_or_404(doc_id)
    if d.project.architect_id != current_user.id: abort(403)
    return redirect(request.referrer or '/dashboard')

@bp.route('/documents/<int:doc_id>/approve', methods=['POST'])
@login_required
def approve(doc_id):
    if current_user.role != 'client': abort(403)
    d = Document.query.get_or_404(doc_id)
    if d.project.client_id != current_user.id: abort(403)
    
    d.approval_status = 'approved'
    d.approved_at = datetime.utcnow()
    db.session.commit()
    return redirect(request.referrer or '/dashboard')

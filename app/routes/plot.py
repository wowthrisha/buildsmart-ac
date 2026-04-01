from flask import Blueprint, request, redirect, jsonify, render_template, abort
from flask_login import login_required, current_user
from app import db
from app.models import Project, PlotData
from app.auth import require_architect
from datetime import datetime

bp = Blueprint('plot', __name__)

@bp.route('/plot')
@login_required
def index():
    require_architect()
    projects = Project.query.filter_by(architect_id=current_user.id).all()
    return render_template('architect/plot_standalone.html', projects=projects)

@bp.route('/projects/<int:project_id>/plot/upload', methods=['POST'])
@login_required
def upload(project_id):
    require_architect()
    try:
        p = Project.query.get_or_404(project_id)
        if current_user.role == 'architect' and p.architect_id != current_user.id:
            abort(403)
        if current_user.role == 'client' and p.client_id != current_user.id:
            abort(403)
            
        file = request.files.get('sketch')
        if file and file.filename:
            ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
            from flask import current_app
            if ext not in current_app.config.get('ALLOWED_EXTENSIONS', {'pdf','jpg','jpeg','png','dwg','dxf'}):
                from flask import flash
                flash('File type not allowed.', 'error')
                return redirect(request.referrer or '/dashboard')
            from werkzeug.utils import secure_filename
            import os
            filename = secure_filename(file.filename)
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

@bp.route('/projects/<int:project_id>/plot/update', methods=['POST'])
@login_required
def update(project_id):
    require_architect()
    try:
        p = Project.query.get_or_404(project_id)
        if current_user.role == 'architect' and p.architect_id != current_user.id:
            abort(403)
            
        plot = p.plot
        if plot:
            from app.tnpcr import compute_compliance, fuzzy_confidence
            import json
            compliance_result = compute_compliance(plot)
            plot.compliance_json = json.dumps(compliance_result)
            plot.fuzzy_score = fuzzy_confidence(compliance_result)
            
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

@bp.route('/projects/<int:project_id>/plot/confirm', methods=['POST'])
@login_required
def confirm(project_id):
    require_architect()
    try:
        p = Project.query.get_or_404(project_id)
        if current_user.role == 'architect' and p.architect_id != current_user.id:
            abort(403)
            
        if p.plot:
            p.plot.confirmed = True
            p.plot.confirmed_at = datetime.utcnow()
            
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

@bp.route('/api/rag/query', methods=['POST'])
@login_required
def rag_query():
    if current_user.role != 'client': abort(403)
    try:
        data = request.get_json() or {}
        question_val = data.get('question') or request.form.get('question') or ''
        question = str(question_val).strip()
        if not question:
            return jsonify({'answer': 'Please enter a question.'}), 400
        from app.rag import query as rag_fn
        ans = rag_fn(question)
        return jsonify({'answer': ans})
    except Exception as e:
        db.session.rollback()
        from flask import current_app
        current_app.logger.error(f'RAG error: {e}')
        return jsonify({'answer': 'Could not process your question. Please try again.', 'error': str(e)}), 500

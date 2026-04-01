from flask import Blueprint, request, redirect, flash, abort, render_template, current_app, send_from_directory
from flask_login import login_required, current_user
import os
from werkzeug.utils import secure_filename
from app import db
from app.models import Project, Payment, User, Notification
from app.auth import require_architect

bp = Blueprint('payments', __name__)

@bp.route('/payments')
@login_required
def index():
    require_architect()
    payments = Payment.query.join(Project).filter(Project.architect_id == current_user.id).all()
    projects = Project.query.filter_by(architect_id=current_user.id).all()
    return render_template('architect/payments_standalone.html', payments=payments, projects=projects)

@bp.route('/projects/<int:project_id>/payments/budget', methods=['POST'])
@login_required
def update_budget(project_id):
    require_architect()
    try:
        p = Project.query.get_or_404(project_id)
        if current_user.role == 'architect' and p.architect_id != current_user.id:
            abort(403)
        p.total_budget = float(request.form.get('total_budget', 0))
        db.session.commit()
        flash('Saved.', 'success')
        return redirect(request.referrer or '/dashboard')
    except ValueError as e:
        db.session.rollback()
        flash(f'Invalid input: {e}', 'error')
        return redirect(request.referrer or '/dashboard')
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error in {request.endpoint}: {e}')
        flash('Something went wrong. Please try again.', 'error')
        return redirect(request.referrer or '/dashboard')

@bp.route('/projects/<int:project_id>/payments/add', methods=['POST'])
@login_required
def add(project_id):
    if current_user.role not in ('architect', 'client'): abort(403)
    try:
        p = Project.query.get_or_404(project_id)
        if current_user.role == 'architect' and p.architect_id != current_user.id:
            abort(403)
        if current_user.role == 'client' and p.client_id != current_user.id:
            abort(403)
            
        amount = float(request.form.get('amount', '0'))
        purpose = request.form.get('purpose', '')[:500]
        if amount > 0:
            payment = Payment(project_id=p.id, amount=amount, purpose=purpose,
                              notes=request.form.get('notes', '')[:1000], logged_by=current_user.id,
                              logged_by_role=current_user.role)
            from datetime import datetime
            payment.date = datetime.utcnow().date()
            db.session.add(payment)
            db.session.commit()
            
            try:
                from app.notifications_service import notify_user, send_whatsapp
                other = p.client if current_user.role == 'architect' else p.architect
                if other:
                    notify_user(other.id, 'Payment logged', f'₹{amount} for {purpose} on {p.name}')
                    if getattr(other, 'phone', None) and getattr(other, 'reminders_sms', None):
                        send_whatsapp(other.phone, f'BuildSmart: ₹{amount} on {p.name}')
            except Exception as notify_e:
                current_app.logger.error(f'Notification error: {notify_e}')
                
        flash('Saved.', 'success')
        return redirect(request.referrer or '/dashboard')
    except ValueError as e:
        db.session.rollback()
        flash(f'Invalid input: {e}', 'error')
        return redirect(request.referrer or '/dashboard')
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error in {request.endpoint}: {e}')
        flash('Something went wrong. Please try again.', 'error')
        return redirect(request.referrer or '/dashboard')

@bp.route('/payments/<int:payment_id>/download')
@login_required
def download_bill(payment_id):
    p_log = Payment.query.get_or_404(payment_id)
    project = p_log.project
    
    # Ownership: owner or architect
    if current_user.role == 'architect' and project.architect_id != current_user.id:
        abort(403)
    if current_user.role == 'client' and project.client_id != current_user.id:
        abort(403)
        
    if not p_log.bill_filename:
        abort(404)
        
    from flask import current_app
    directory = current_app.config['UPLOAD_FOLDER']
    return send_from_directory(directory, p_log.bill_filename, as_attachment=True)

from flask import Blueprint, request, redirect, render_template, abort, flash
from flask_login import login_required, current_user
from app import db
from app.models import Project, Meeting
from app.auth import require_architect
from datetime import datetime

bp = Blueprint('meetings', __name__)

@bp.route('/meetings')
@login_required
def index():
    require_architect()
    meetings = Meeting.query.join(Project).filter(Project.architect_id == current_user.id).all()
    projects = Project.query.filter_by(architect_id=current_user.id).all()
    return render_template('architect/meetings_standalone.html', meetings=meetings, projects=projects)

@bp.route('/projects/<int:project_id>/meetings/propose', methods=['POST'])
@login_required
def propose(project_id):
    require_architect()
    try:
        p = Project.query.get_or_404(project_id)
        if current_user.role == 'architect' and p.architect_id != current_user.id:
            abort(403)
            
        slot = request.form.get('slot_1')
        if slot:
            val = datetime.strptime(slot, '%Y-%m-%dT%H:%M') if 'T' in slot else datetime.strptime(slot, '%Y-%m-%d %H:%M')
            m = Meeting(project_id=p.id, slot_1=val, status='proposed')
            db.session.add(m)
            db.session.commit()
            
            try:
                from app.notifications_service import notify_user
                if p.client:
                    notify_user(p.client_id, 'Meeting proposed', f'Your architect has proposed meeting slots for {p.name}.')
            except Exception as e:
                from flask import current_app
                current_app.logger.error(f'Notification error: {e}')
                
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

@bp.route('/meetings/<int:meeting_id>/confirm', methods=['POST'])
@login_required
def confirm(meeting_id):
    try:
        m = Meeting.query.get_or_404(meeting_id)
        p = m.project
        if current_user.role == 'architect' and p.architect_id != current_user.id:
            abort(403)
        if current_user.role == 'client' and p.client_id != current_user.id:
            abort(403)
            
        m.status = 'confirmed'
        m.confirmed_slot = m.slot_1
        m.confirmed_at = datetime.utcnow()
        db.session.commit()
        
        from flask import flash, url_for
        flash('Saved.', 'success')
        if current_user.role == 'client':
            return redirect(url_for('client.meetings'))
        return redirect(url_for('projects.workspace', project_id=m.project_id) + '#meetings')
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

@bp.route('/meetings/<int:meeting_id>/notes', methods=['POST'])
@login_required
def notes(meeting_id):
    require_architect()
    try:
        m = Meeting.query.get_or_404(meeting_id)
        if m.project.architect_id != current_user.id:
            abort(403)
            
        m.mom_content = request.form.get('mom_content', '').strip()
        m.mom_date = datetime.utcnow()
        db.session.commit()
        
        from flask import flash, url_for
        flash('Minutes of meeting saved.', 'success')
        return redirect(request.referrer or url_for('projects.workspace', project_id=m.project_id) + '#meetings')
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

@bp.route('/meetings/<int:meeting_id>/counter', methods=['POST'])
@login_required
def counter(meeting_id):
    try:
        m = Meeting.query.get_or_404(meeting_id)
        p = m.project
        if current_user.role != 'client' or p.client_id != current_user.id:
            abort(403)
            
        counter_slot_str = request.form.get('counter_slot')
        if not counter_slot_str:
            flash('Please provide a counter-proposal slot.', 'error')
            return redirect(request.referrer or '/my_project/meetings')
            
        try:
            m.counter_slot = datetime.strptime(counter_slot_str, '%Y-%m-%dT%H:%M') if 'T' in counter_slot_str else datetime.strptime(counter_slot_str, '%Y-%m-%d %H:%M')
        except ValueError:
            flash('Invalid date/time format.', 'error')
            return redirect(request.referrer or '/my_project/meetings')

        m.status = 'countered'
        db.session.commit()
        
        try:
            from app.notifications_service import notify_user
            notify_user(p.architect_id, 'Meeting Countered', f'Client has proposed an alternative slot for {p.name}.')
        except Exception as e:
            from flask import current_app
            current_app.logger.error(f'Notification error: {e}')
            
        flash('Counter-proposal sent to architect.', 'success')
        return redirect('/my_project/meetings')
    except Exception as e:
        db.session.rollback()
        from flask import current_app, flash
        current_app.logger.error(f'Error in {request.endpoint}: {e}')
        flash('Something went wrong. Please try again.', 'error')
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

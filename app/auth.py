from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db, limiter
from app.models import User, AuditLog
from datetime import datetime

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET','POST'])
@limiter.limit("10 per minute", methods=["POST"])
def login():
    if current_user.is_authenticated:
        return _redirect_by_role(current_user)
    if request.method == 'POST':
        try:
            email    = request.form.get('email','').strip().lower()
            password = request.form.get('password','')
            user     = User.query.filter_by(email=email).first()
            if user and user.check_password(password):
                login_user(user, remember=True)
                # Audit
                log = AuditLog(project_id=None, actor_id=user.id,
                               action='LOGIN', description=f'{user.name} logged in',
                               is_client_visible=False)
                db.session.add(log)
                db.session.commit()
                return _redirect_by_role(user)
            flash('Invalid email or password.', 'error')
        except Exception as e:
            db.session.rollback()
            from flask import current_app
            current_app.logger.error(f'Login error: {e}')
            flash('Something went wrong. Please try again.', 'error')
    return render_template('auth/login.html')

def _redirect_by_role(user):
    if user.role == 'architect':
        return redirect(url_for('projects.dashboard'))
    return redirect(url_for('client.portal'))

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@bp.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return _redirect_by_role(current_user)
    if request.method == 'POST':
        name = request.form.get('name', '').strip()[:100]
        email = request.form.get('email', '').strip().lower()[:254]
        password = request.form.get('password', '')

        # Input validation
        if not name:
            flash('Name is required.', 'error')
            return redirect(url_for('auth.register'))
        if '@' not in email or '.' not in email.split('@')[-1]:
            flash('Please enter a valid email address.', 'error')
            return redirect(url_for('auth.register'))
        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'error')
            return redirect(url_for('auth.register'))

        # Role is ALWAYS 'client' on self-registration.
        # Architects are created by admin only.
        role = 'client'
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'error')
            return redirect(url_for('auth.register'))
            
        user = User(name=name, email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        # Log registration
        log = AuditLog(project_id=None, actor_id=user.id, action='REGISTER', 
                       description=f'New {role} registered: {name}')
        db.session.add(log)
        db.session.commit()
        
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/register.html')

# Role guards
def require_architect():
    from flask_login import current_user
    from flask import abort
    if not current_user.is_authenticated or current_user.role != 'architect':
        abort(403)

def require_client():
    from flask_login import current_user
    from flask import abort
    if not current_user.is_authenticated or current_user.role != 'client':
        abort(403)


from flask import Blueprint, request, redirect, jsonify, render_template, abort
from flask_login import login_required, current_user
from app import db
from app.models import Project, ComplianceItem
from app.auth import require_architect
from datetime import datetime

bp = Blueprint('compliance', __name__)

@bp.route('/compliance')
@login_required
def index():
    require_architect()
    projects = Project.query.filter_by(architect_id=current_user.id).all()
    return render_template('architect/compliance_standalone.html', projects=projects)

@bp.route('/projects/<int:project_id>/compliance/<int:item_id>/toggle', methods=['POST'])
@login_required
def toggle(project_id, item_id):
    try:
        p = Project.query.get_or_404(project_id)
        if current_user.role == 'architect' and p.architect_id != current_user.id:
            abort(403)
        if current_user.role == 'client' and p.client_id != current_user.id:
            abort(403)
            
        item = ComplianceItem.query.get_or_404(item_id)
        if item.project_id != p.id: abort(404)
        
        from datetime import datetime
        role = current_user.role
        if role == 'architect':
            item.arch_checked = not bool(item.arch_checked)
            item.arch_checked_at = datetime.utcnow() if item.arch_checked else None
            item.checked = item.arch_checked
        elif role == 'client':
            item.client_checked = not bool(item.client_checked)
            item.client_checked_at = datetime.utcnow() if item.client_checked else None
            
        db.session.commit()
        return jsonify({
            'ok': True,
            'arch_checked': bool(item.arch_checked),
            'client_checked': bool(item.client_checked),
            'both_done': bool(item.arch_checked and item.client_checked)
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'ok': False, 'error': str(e)}), 500

@bp.route('/projects/<int:project_id>/compliance/add-custom', methods=['POST'])
@login_required
def add_custom(project_id):
    require_architect()
    try:
        p = Project.query.get_or_404(project_id)
        if current_user.role == 'architect' and p.architect_id != current_user.id:
            abort(403)
            
        data = request.form
        if request.is_json: data = request.get_json()
        label = (data.get('label') or data.get('name') or '').strip()[:100]
        desc = data.get('description', '').strip()[:500]
        if label:
            item = ComplianceItem(project_id=p.id, item=label, label=label, is_custom=True, description=desc)
            db.session.add(item)
            db.session.commit()
            return jsonify({'ok': True, 'id': item.id, 'label': item.label or item.item})
        return jsonify({'ok': False, 'error': 'No label provided'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'ok': False, 'error': str(e)}), 500

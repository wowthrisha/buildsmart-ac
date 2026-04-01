from app import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id              = db.Column(db.Integer, primary_key=True)
    name            = db.Column(db.String(120), nullable=False)
    email           = db.Column(db.String(120), unique=True, nullable=False)
    password_hash   = db.Column(db.String(256), nullable=False)
    role            = db.Column(db.String(20), nullable=False)  # 'architect' | 'client'
    phone           = db.Column(db.String(20))
    reminders_email = db.Column(db.Boolean, default=True)
    reminders_sms   = db.Column(db.Boolean, default=False)
    created_at      = db.Column(db.DateTime, default=datetime.utcnow)

    notifications   = db.relationship('Notification', backref='user', lazy='dynamic')

    # Helper
    @property
    def initials(self):
        parts = self.name.split()
        return (parts[0][0] + (parts[-1][0] if len(parts) > 1 else '')).upper()

    def set_password(self, pw): self.password_hash = generate_password_hash(pw)
    def check_password(self, pw): return check_password_hash(self.password_hash, pw)

class Project(db.Model):
    id           = db.Column(db.Integer, primary_key=True)
    name         = db.Column(db.String(200), nullable=False)
    status       = db.Column(db.String(30), default='Design')
    # status values: Design | Review | Submitted | Approved
    plot_zone    = db.Column(db.String(50))
    architect_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    client_id    = db.Column(db.Integer, db.ForeignKey('user.id'))
    total_budget     = db.Column(db.Float, default=0.0)
    allow_client_compliance = db.Column(db.Boolean, default=False)
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at   = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    architect    = db.relationship('User', foreign_keys=[architect_id])
    client       = db.relationship('User', foreign_keys=[client_id])
    plot         = db.relationship('PlotData', backref='project', uselist=False)
    documents    = db.relationship('Document', backref='project', lazy='dynamic')
    meetings     = db.relationship('Meeting', backref='project', lazy='dynamic')
    payments     = db.relationship('Payment', backref='project', lazy='dynamic')
    checklist    = db.relationship('ComplianceItem', backref='project', lazy='dynamic')
    audit_logs   = db.relationship('AuditLog', backref='project', lazy='dynamic')
    images       = db.relationship('ProjectImage', backref='project', lazy='dynamic')

    STATUS_ORDER = ['Design', 'Review', 'Submitted', 'Approved']

    @property
    def stage_index(self):
        try: return self.STATUS_ORDER.index(self.status)
        except ValueError: return 0

class PlotData(db.Model):
    id             = db.Column(db.Integer, primary_key=True)
    project_id     = db.Column(db.Integer, db.ForeignKey('project.id'), unique=True)
    # Sketch
    sketch_filename= db.Column(db.String(255))
    sketch_uploader= db.Column(db.String(10))  # 'architect' | 'client'
    # Dimensions (architect edits / confirms)
    area           = db.Column(db.Float)
    frontage       = db.Column(db.Float)
    depth          = db.Column(db.Float)
    road_width     = db.Column(db.Float)
    front_setback  = db.Column(db.Float)
    rear_setback   = db.Column(db.Float)
    side_setback   = db.Column(db.Float)
    height         = db.Column(db.Float)
    built_up_area  = db.Column(db.Float)
    # OCR confidence per field (0.0–1.0, -1 = manually entered)
    conf_area      = db.Column(db.Float, default=-1)
    conf_frontage  = db.Column(db.Float, default=-1)
    conf_depth     = db.Column(db.Float, default=-1)
    conf_setback   = db.Column(db.Float, default=-1)
    # Confirmation gate
    confirmed      = db.Column(db.Boolean, default=False)
    confirmed_at   = db.Column(db.DateTime)
    # Fuzzy compliance (computed, stored as JSON string)
    compliance_json= db.Column(db.Text)   # {"area":"pass","frontage":"warn","setback":"fail",...}
    fuzzy_score    = db.Column(db.Float, nullable=True)  # 0–100 computed confidence score
    # Track detection
    track          = db.Column(db.String(2))  # 'A' or 'B'
    updated_at     = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Document(db.Model):
    id              = db.Column(db.Integer, primary_key=True)
    project_id      = db.Column(db.Integer, db.ForeignKey('project.id'))
    filename        = db.Column(db.String(255), nullable=False)
    original_name   = db.Column(db.String(255))
    category        = db.Column(db.String(50))  # Site Plan|Structural|Legal|Client Docs
    uploader_id     = db.Column(db.Integer, db.ForeignKey('user.id'))
    uploader_role   = db.Column(db.String(10))  # 'architect' | 'client'
    shared_with_client = db.Column(db.Boolean, default=False)
    approval_status = db.Column(db.String(20), default='none')  # none|pending|approved|commented
    approved_at     = db.Column(db.DateTime)
    approval_comment= db.Column(db.Text)
    created_at      = db.Column(db.DateTime, default=datetime.utcnow)

    uploader        = db.relationship('User', foreign_keys=[uploader_id])
    versions        = db.relationship('DocumentVersion', backref='document',
                                      order_by='DocumentVersion.created_at',
                                      lazy='dynamic')

    @property
    def current_version(self):
        return self.versions.order_by(DocumentVersion.created_at.desc()).first()

    @property
    def version_label(self):
        labels = ['Rev A','Rev B','Rev C','Rev D','Rev E','Rev F','Rev G','Rev H']
        count  = self.versions.count()
        return labels[count - 1] if count <= len(labels) else f'Rev {count}'

class DocumentVersion(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('document.id'))
    filename    = db.Column(db.String(255))
    version_num = db.Column(db.Integer)
    uploader_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    uploader    = db.relationship('User')

    VERSION_LABELS = ['Rev A','Rev B','Rev C','Rev D','Rev E','Rev F','Rev G','Rev H']

    @property
    def label(self):
        idx = self.version_num - 1
        return self.VERSION_LABELS[idx] if idx < len(self.VERSION_LABELS) else f'Rev {self.version_num}'

class ComplianceItem(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    item       = db.Column(db.String(100))  # patta|ec|site_plan|scheme|self_cert|id_proof|noc
    label      = db.Column(db.String(100))
    checked    = db.Column(db.Boolean, default=False)
    checked_at = db.Column(db.DateTime)
    checked_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    # Dual-role checkbox support + custom item fields
    arch_checked      = db.Column(db.Boolean, default=False, nullable=True)
    client_checked    = db.Column(db.Boolean, default=False, nullable=True)
    arch_checked_at   = db.Column(db.DateTime, nullable=True)
    client_checked_at = db.Column(db.DateTime, nullable=True)
    is_custom         = db.Column(db.Boolean, default=False, nullable=True)
    description       = db.Column(db.Text, nullable=True)

COMPLIANCE_ITEMS = [
    ('patta',      'Patta'),
    ('ec',         'EC (Encumbrance Certificate)'),
    ('site_plan',  'Signed Site Plan'),
    ('scheme',     'Scheme Drawings'),
    ('self_cert',  'Self-Certification Form'),
    ('id_proof',   'ID Proof'),
    ('noc',        'NOC (if applicable)'),
]

class Meeting(db.Model):
    id              = db.Column(db.Integer, primary_key=True)
    project_id      = db.Column(db.Integer, db.ForeignKey('project.id'))
    status          = db.Column(db.String(20), default='proposed')
    # proposed | awaiting_client | confirmed | cancelled
    slot_1          = db.Column(db.DateTime)
    slot_2          = db.Column(db.DateTime)
    slot_3          = db.Column(db.DateTime)
    confirmed_slot  = db.Column(db.DateTime)
    confirmed_at    = db.Column(db.DateTime)
    counter_count   = db.Column(db.Integer, default=0)  # max 2 counters allowed
    counter_slot    = db.Column(db.DateTime, nullable=True)  # client's proposed alternative
    mom_discussion  = db.Column(db.Text)
    mom_decision    = db.Column(db.Text)
    mom_client_notes= db.Column(db.Text)
    mom_content     = db.Column(db.Text, nullable=True)      # combined MOM text
    mom_date        = db.Column(db.DateTime, nullable=True)   # when MOM was logged
    created_at      = db.Column(db.DateTime, default=datetime.utcnow)

    action_items    = db.relationship('ActionItem', backref='meeting', lazy='dynamic')
    reminders       = db.relationship('MeetingReminder', backref='meeting', lazy='dynamic')

class ActionItem(db.Model):
    id           = db.Column(db.Integer, primary_key=True)
    meeting_id   = db.Column(db.Integer, db.ForeignKey('meeting.id'))
    project_id   = db.Column(db.Integer, db.ForeignKey('project.id'))
    description  = db.Column(db.Text, nullable=False)
    assigned_to  = db.Column(db.Integer, db.ForeignKey('user.id'))
    due_date     = db.Column(db.Date)
    status       = db.Column(db.String(20), default='pending')  # pending | complete
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)

    assignee     = db.relationship('User')

class MeetingReminder(db.Model):
    id           = db.Column(db.Integer, primary_key=True)
    meeting_id   = db.Column(db.Integer, db.ForeignKey('meeting.id'))
    trigger_at   = db.Column(db.DateTime)
    sent         = db.Column(db.Boolean, default=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    recipient    = db.relationship('User')

class Payment(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    amount     = db.Column(db.Float, nullable=False)
    date       = db.Column(db.Date, nullable=False)
    purpose    = db.Column(db.String(50))  # advance | milestone | final
    bill_filename = db.Column(db.String(255))
    notes      = db.Column(db.Text)
    logged_by  = db.Column(db.Integer, db.ForeignKey('user.id'))
    logged_by_role = db.Column(db.String(10), nullable=True, default='architect')  # 'architect' | 'client'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AuditLog(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    actor_id   = db.Column(db.Integer, db.ForeignKey('user.id'))
    action     = db.Column(db.String(50))   # UPLOAD|UPDATE|DELETE|SHARE|APPROVE|LOGIN|CONFIRM
    description= db.Column(db.Text)
    is_client_visible = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    actor      = db.relationship('User')

class ProjectImage(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    project_id  = db.Column(db.Integer, db.ForeignKey('project.id'))
    filename    = db.Column(db.String(255))
    tag         = db.Column(db.String(50))  # 3D Render | Drawing | Reference
    uploader_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    uploader    = db.relationship('User')

class Notification(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey('user.id'))
    title      = db.Column(db.String(120))
    body       = db.Column(db.Text)
    read       = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

import os
from dotenv import load_dotenv
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY             = os.environ.get('SECRET_KEY', 'dev-secret-key-12345')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'buildsmart.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER          = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')
    MAX_CONTENT_LENGTH     = 20 * 1024 * 1024   # 20 MB
    ALLOWED_EXTENSIONS     = {'pdf','jpg','jpeg','png','dwg','dxf'}
    WTF_CSRF_ENABLED       = True
    # Security cookie flags (P2-16)
    SESSION_COOKIE_SECURE  = os.environ.get('FLASK_ENV') == 'production'  # HTTPS only in prod
    SESSION_COOKIE_HTTPONLY= True   # JS cannot access cookie
    SESSION_COOKIE_SAMESITE= 'Lax'  # CSRF protection
    # Debug flag (P3-D)
    DEBUG                  = os.environ.get('FLASK_DEBUG', 'False').lower() in ['true', '1']
    # Email (optional — Gmail App Password)
    MAIL_SERVER            = 'smtp.gmail.com'
    MAIL_PORT              = 587
    MAIL_USE_TLS           = True
    MAIL_USERNAME          = os.environ.get('GMAIL_USER', '')
    MAIL_PASSWORD          = os.environ.get('GMAIL_APP_PASSWORD', '')

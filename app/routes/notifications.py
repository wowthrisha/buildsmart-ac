from flask import Blueprint, Response, stream_with_context
from flask_login import login_required

bp = Blueprint('notifications', __name__)

@bp.route('/notifications/stream')
@login_required
def stream():
    def generate():
        yield "data: keep-alive\n\n"
    return Response(stream_with_context(generate()), mimetype='text/event-stream')

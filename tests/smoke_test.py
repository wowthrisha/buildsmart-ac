import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import User, Project

def test_app():
    app = create_app()
    with app.app_context():
        # Check tables
        try:
            users_count = User.query.count()
            projects_count = Project.query.count()
            print(f"SMOKE TEST SUCCESS: Found {users_count} users and {projects_count} projects.")
            return True
        except Exception as e:
            print(f"SMOKE TEST FAILED: {e}")
            return False

if __name__ == "__main__":
    if test_app():
        sys.exit(0)
    else:
        sys.exit(1)

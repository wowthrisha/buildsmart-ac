import sqlite3
import os

db_path = os.path.join('instance', 'buildsmart.db')

if not os.path.exists(db_path):
    print("Error: Could not find instance/buildsmart.db")
    exit(1)

try:
    db = sqlite3.connect(db_path)
    
    # Check if we need to add mom_content
    cursor = db.cursor()
    cursor.execute("PRAGMA table_info(meeting)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if 'mom_content' not in columns:
        db.execute('ALTER TABLE meeting ADD COLUMN mom_content TEXT')
        print("✅ Added 'mom_content' to meeting table.")
    else:
        print("ℹ️ 'mom_content' already exists.")
        
    if 'mom_date' not in columns:
        db.execute('ALTER TABLE meeting ADD COLUMN mom_date DATETIME')
        print("✅ Added 'mom_date' to meeting table.")
    else:
        print("ℹ️ 'mom_date' already exists.")
        
    db.commit()
    print("Database patching complete! You can now run the app.")
except Exception as e:
    print(f"Error patching database: {e}")
finally:
    db.close()

from app import create_app, db
from app.models import User, Project, ComplianceItem, COMPLIANCE_ITEMS
from datetime import date

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # Architect
    priya = User(name='Priya Architect', email='priya@buildsmartdemo.in', role='architect')
    priya.set_password('architect123')
    db.session.add(priya)

    # Client
    ramesh = User(name='Ramesh Owner', email='ramesh@buildsmartdemo.in', role='client', phone='+919876543210')
    ramesh.set_password('client123')
    db.session.add(ramesh)

    db.session.flush()  # get IDs

    # Sample project
    p = Project(name='Ramesh Residence', status='Design',
                plot_zone='Residential', architect_id=priya.id, client_id=ramesh.id)
    db.session.add(p)
    db.session.flush()

    # Seed compliance checklist
    for item_key, item_label in COMPLIANCE_ITEMS:
        db.session.add(ComplianceItem(project_id=p.id, item=item_key, label=item_label))

    db.session.commit()
    print('✅  Seeded: priya@buildsmartdemo.in / architect123')
    print('✅  Seeded: ramesh@buildsmartdemo.in / client123')
    print(f'✅  Project: {p.name} (id={p.id})')

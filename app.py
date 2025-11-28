from flask import Flask
from application.database import db
app = None

def create_app():
    app = Flask(__name__)
    app.debug = True
    app.secret_key = 'hospital-db'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
    db.init_app(app)
    app.app_context().push()
    return app

app = create_app()
from application.controllers import *
if __name__=="__main__":
    with app.app_context():
        db.create_all()
        Admin1 = Admin.query.filter_by(username='admin').first()
        if not Admin1:
            Admin1 = Admin(username='admin', email='admin@example.com', password='admin')
            db.session.add(Admin1)
            db.session.commit()
        DEFAULT_DEPARTMENTS = [
            {"dep_name": "Cardiology", "description": "Heart and blood vessel diseases"},
            {"dep_name": "Neurology", "description": "Brain, spine and nervous system disorders"},
            {"dep_name": "Orthopedics", "description": "Bones, joints, muscles and fractures"},
            {"dep_name": "General", "description": "Primary care and internal medicine"},
            {"dep_name": "Pediatrics", "description": "Medical care for children and infants"},
        ]
        if Department.query.count() == 0:
            for dept in DEFAULT_DEPARTMENTS:
                department = Department(
                    dep_name=dept["dep_name"],
                    description=dept["description"]
                )
                db.session.add(department)
            db.session.commit()
    app.run()
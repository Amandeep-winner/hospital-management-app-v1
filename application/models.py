from .database import db

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), unique=True, nullable=False)
    username = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), unique=True, nullable=False)
    username = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    name = db.Column(db.String(), nullable=False)
    Dep_id = db.Column(db.Integer, db.ForeignKey("department.id"), nullable=False)
    gender = db.Column(db.Enum('Male', 'Female'), nullable=False)
    appointments = db.relationship('Appointment', backref='doctor')

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), unique=True, nullable=False)
    username = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    name = db.Column(db.String(), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.Enum('Male', 'Female'))
    appointments = db.relationship('Appointment', backref='patient')

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    p_id = db.Column(db.Integer, db.ForeignKey("patient.id"), nullable=False)
    d_id = db.Column(db.Integer, db.ForeignKey("doctor.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    status = db.Column(db.Enum('Booked', 'Completed', 'Cancelled'), nullable=False)
    treatments = db.relationship('Treatment', backref='appointment')

class Treatment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appoint_id = db.Column(db.Integer, db.ForeignKey("appointment.id"), nullable=False)
    diagnosis = db.Column(db.String(), nullable=False)
    prescription = db.Column(db.String(), nullable=False)
    notes = db.Column(db.String())

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dep_name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    doctors_registered = db.relationship('Doctor', backref='department')

from datetime import datetime
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
    is_blacklisted = db.Column(db.Boolean, default=False, nullable=False)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), unique=True, nullable=False)
    username = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    name = db.Column(db.String(), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.Enum('Male', 'Female'))
    appointments = db.relationship('Appointment', backref='patient')
    is_blacklisted = db.Column(db.Boolean, default=False, nullable=False)

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
    appoint_id = db.Column(db.Integer, db.ForeignKey('appointment.id'), nullable=False)
    diagnosis = db.Column(db.Text, nullable=False)
    prescription = db.Column(db.Text, nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    medicines = db.relationship('Medicine', backref='treatment', cascade='all, delete-orphan')

class Medicine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    treatment_id = db.Column(db.Integer, db.ForeignKey('treatment.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    dosage = db.Column(db.String(50))
    duration = db.Column(db.String(50))

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dep_name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    doctors_registered = db.relationship('Doctor', backref='department')

class DoctorAvailability(db.Model):
    __tablename__ = 'doctor_availability'
    
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    morning_slot = db.Column(db.Boolean, default=False)   # 08:00 - 12:00 am
    evening_slot = db.Column(db.Boolean, default=False)   # 04:00 - 09:00 pm

    # One doctor can't have duplicate dates
    __table_args__ = (db.UniqueConstraint('doctor_id', 'date', name='unique_doctor_date'),)
    doctor = db.relationship('Doctor', backref='availability')
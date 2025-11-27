from .database import db
from werkzeug.security import generate_password_hash

def create_default_admin():
    # check if an admin already exists
    existing = Admin.query.filter_by(username="Meghna").first()
    if existing:
        return
    
    admin = Admin(
        username="Meghna",
        password=generate_password_hash("Meghna@07"),  
        type="admin"
    )
    db.session.add(admin)
    db.session.commit()
    
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    type = db.Column(db.String(), nullable=False, default="admin")
   
    
class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)
    description = db.Column(db.String())
    doctors = db.relationship('Doctor', backref='department', lazy=True)
    @property
    def doctors_registered(self):
        return len(self.doctors)

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    specialization = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    experience=db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(), nullable=False, default="doctor")
    full_name = db.Column(db.String(), nullable=False)
    bio = db.Column(db.String())
    appointments = db.relationship('Appointment', backref='doctor',lazy=True)
    availability = db.relationship("Availability", backref="doctor", lazy=True)
        

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    type = db.Column(db.String(), nullable=False, default="patient")
    appointments = db.relationship('Appointment', backref='patient', lazy=True)
    contact = db.Column(db.String(),  unique=True)
    full_name = db.Column(db.String())

    
    
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time_start = db.Column(db.Time, nullable=False)
    appointment_time_end = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(), nullable=False, default="Scheduled")
    treatment = db.relationship('Treatment', backref='appointment', uselist=False)

class Treatment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'), nullable=False, unique=True)
    diagnosis = db.Column(db.String(), nullable=False)
    prescription = db.Column(db.String(), nullable=False)
    notes = db.Column(db.String())
    medicines = db.Column(db.String())
    visit_type = db.Column(db.String(), nullable=False)
    tests_done = db.Column(db.String())

class Availability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    morning_available = db.Column(db.Boolean, default=False)
    evening_available = db.Column(db.Boolean, default=False)

    
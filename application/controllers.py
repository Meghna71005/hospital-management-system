from flask import Flask, render_template, url_for, redirect, request, flash, session
from flask import current_app as app
from .models import *
from werkzeug.security import generate_password_hash, check_password_hash
@app.route("/")
def home():
    if 'user_id' in session:
        return render_template("index.html", active="home")
    else:
        return redirect(url_for('login'))
    
@app.route("/login", methods=['GET', 'POST'])
def login():
     if request.method == 'POST':
        username= request.form['username']
        password= request.form.get('password')
        
        if not username or not password :
            flash("Please fill in all fields.", "error")
            return redirect(url_for('login'))
        
        this_user = Admin.query.filter_by(username=username).first()
        if not this_user:
            # Check Doctor
            this_user = Doctor.query.filter_by(username=username).first()
        if not this_user:
            # Check Patient
            this_user = Patient.query.filter_by(username=username).first()

        if this_user:
            if check_password_hash(this_user.password, password):
                session['user_id'] = this_user.id
                session['user_type'] = this_user.type
                if this_user.type=="admin":
                   
                    return redirect(url_for('admin'))
                elif this_user.type=="doctor":
                    
                    return redirect(url_for('doctor_dashboard', doctor_id=this_user.id))
                elif this_user.type=="patient":
                    
                    return redirect(url_for('patient', patient_id=this_user.id))
            else:
                return render_template("incorrect_password.html")
        else:
            return render_template("user_not_found.html")
       
     return render_template("login.html", active="login")

@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        username = request.form.get("username")
        return render_template("forgot_password_submitted.html", username=username)
    return render_template("forgot_password.html")

@app.route("/register", methods=['GET', 'POST'])
def register() :
    if request.method == 'POST':
        username= request.form['username']
        password= request.form.get('password')
        contact= request.form.get('contact')
        confirm_password= request.form.get('confirm-password') 
        user_name = Patient.query.filter_by(username=username).first()
        user_contact = Patient.query.filter_by(contact=contact).first()
        
        if not username or not password or not confirm_password:
            flash("Please fill in all fields.", "error")
            return redirect(url_for('register'))
        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return redirect(url_for('register'))
        if user_name or user_contact:
            return render_template("already_registered.html", error="Username already exists!")
       
        password_hash = generate_password_hash(password)
        # Create Patient object
        new_patient = Patient(
            username=username,
            password=password_hash,
            contact= contact,
            type="patient"
        )

        db.session.add(new_patient)
        db.session.commit()

        return redirect(url_for('login'))    
    return render_template("register.html", active="register")

@app.route("/logout")
def logout():
    session.pop('user_id')
    return redirect(url_for('login'))


from datetime import date

@app.route("/admin")
def admin():
    if session.get('user_type') != 'admin':
        return redirect(url_for('login'))
    user_id = session.get('user_id')
    this_user = Admin.query.get(user_id)
    all_doctors= Doctor.query.all()
    all_patients= Patient.query.all()
    today=date.today()
    up_appoint=(Appointment.query.filter(Appointment.appointment_date >= today).order_by(Appointment.appointment_date, Appointment.appointment_time).all())
    return render_template("admin_dashboard.html",this_user=this_user, all_doctors=all_doctors, all_patients=all_patients, all_appointments=up_appoint)

@app.route("/patient/<int:patient_id>")
def patient(patient_id):
    if session.get('user_type') != 'patient' or session.get('user_id') != patient_id:
        return redirect(url_for('login'))
    this_user=Patient.query.get(patient_id)
    if not this_user:
        return render_template("user_not_found.html")
    my_appointments = Appointment.query.filter_by(patient_id=patient_id).all()
    all_departments = Department.query.all()
    return render_template("patient_dashboard.html", this_user=this_user, all_appointments=my_appointments, all_departments=all_departments)

@app.route("/doctor_dashboard/<int:doctor_id>")
def doctor_dashboard(doctor_id):
    if session.get('user_type') != 'doctor' or session.get('user_id') != doctor_id:
        return redirect(url_for('login'))
    this_user=Doctor.query.get(doctor_id)
    my_appointments = Appointment.query.filter_by(doctor_id=doctor_id).all()
    my_patient_ids = list({appt.patient_id for appt in my_appointments})
    my_patients = Patient.query.filter(Patient.id.in_(my_patient_ids)).all()
    return render_template("doctor_dashboard.html", this_user=this_user, all_appointments=my_appointments, all_patients=my_patients)

@app.route("/add_doctor", methods=["GET", "POST"])
def add_doctor():
    if session.get('user_type') != 'admin':
        return redirect(url_for('login'))
    if request.method == "POST":
        fullname = request.form.get("fullname")
        specialization = request.form.get("specialization")
        experience = request.form.get("experience")

        # Create a new Doctor object
        new_doctor = Doctor(
            username=fullname.lower().replace(" ", "_"),  # Simple username generation
            password=generate_password_hash("doc123"),  
            full_name=fullname,
            specialization=specialization,
            experience=int(experience),
            type="doctor"
        )

        db.session.add(new_doctor)
        db.session.commit()

        return redirect(url_for('admin'))
    return render_template("add_doctor.html")

@app.route("/patient_history_from_dashboard")
def patient_history_from_dashboard():
    this_user_id = session.get('user_id')
    if this_user_id is None or session.get('user_type') != 'patient':
        return redirect(url_for('login'))
    this_user = Patient.query.get(this_user_id)
    all_appointments = Appointment.query.filter_by(patient_id=this_user_id).all()
    return render_template("patient_history.html", back_url=url_for('patient', patient_id=this_user_id), this_user=this_user, all_appointments=all_appointments)

@app.route("/patient_history_from_appointments")
def patient_history_from_appointments():
    return render_template("patient_history.html", back_url=url_for('admin'))  # Replace with your appointments endpoint



@app.route("/back_btn_admin")
def back_btn_admin():
    return render_template("admin_dashboard.html")

@app.route("/update_patients_history")
def update_patient_history():
    return render_template("update_patients_history.html")

@app.route("/doctor_availability")
def doctor_availability():
    return render_template("doctor_availability.html")

@app.route("/dr_avail")
def dr_avail():
    return render_template("dr-avail.html")

@app.route("/view_details")
def view_details():
    return render_template("view_details.html")

@app.route("/dr_detail_card")
def dr_detail_card():
    return render_template("dr-detail-card.html")


    
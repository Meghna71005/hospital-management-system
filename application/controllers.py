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
            
        if this_user and not getattr(this_user, "is_active", True):
            return render_template("user_not_found.html")  # or a “account deactivated” page

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
    session.clear()
    return redirect(url_for('login'))


from datetime import date

@app.route("/admin")
def admin():
    if session.get('user_type') != 'admin':
        return redirect(url_for('login'))
    user_id = session.get('user_id')
    this_user = Admin.query.get(user_id)
    all_doctors = Doctor.query.filter_by(is_active=True).all()
    all_patients = Patient.query.filter_by(is_active=True).all()

    today=date.today()
    up_appoint = (Appointment.query
              .filter_by(status="Scheduled")
              .order_by(Appointment.appointment_date)
              .all())
    print("up_appoint count:", len(up_appoint))

    return render_template("admin_dashboard.html",this_user=this_user, all_doctors=all_doctors, all_patients=all_patients, all_appointments=up_appoint)

from datetime import date
@app.route("/patient/<int:patient_id>")
def patient(patient_id):
    if session.get('user_type') != 'patient' or session.get('user_id') != patient_id:
        return redirect(url_for('login'))
    this_user=Patient.query.get(patient_id)
    if not this_user:
        return render_template("user_not_found.html")

    my_appointments = (Appointment.query
                    .filter_by(patient_id=patient_id, status="Scheduled")
                    .filter(Appointment.appointment_date >= date.today())
                    .order_by(Appointment.appointment_date)
                    .all())

    all_departments = Department.query.all()
    print("Departments count:", len(all_departments)) 
    return render_template("patient_dashboard.html", this_user=this_user, all_appointments=my_appointments, all_departments=all_departments)

@app.route("/doctor_dashboard/<int:doctor_id>")
def doctor_dashboard(doctor_id):
    if session.get('user_type') != 'doctor' or session.get('user_id') != doctor_id:
        return redirect(url_for('login'))
    this_user=Doctor.query.get(doctor_id)
    my_appointments = (Appointment.query
                   .filter_by(doctor_id=doctor_id, status="Scheduled")
                   .order_by(Appointment.appointment_date)
                   .all())

    my_patient_ids = list({appt.patient_id for appt in my_appointments})
    my_patients = Patient.query.filter(Patient.id.in_(my_patient_ids)).all()
    return render_template("doctor_dashboard.html", this_user=this_user, all_appointments=my_appointments, all_patients=my_patients)

@app.route("/add_doctor", methods=["GET", "POST"])
def add_doctor():
    if session.get('user_type') != 'admin':
        return redirect(url_for('login'))
    if request.method == "POST":
        fullname = request.form.get("fullname")
        specialization = int(request.form.get("specialization"))
        experience = int(request.form.get("experience"))

        # Create a new Doctor object
        new_doctor = Doctor(
            username=fullname,  # Simple username generation
            password=generate_password_hash("doc123"),  
            full_name=fullname,
            specialization=specialization,
            experience=int(experience),
            type="doctor",
            photo_filename=""
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

@app.route("/patient_history_from_appointments/<int:patient_id>")
def patient_history_from_appointments(patient_id):
    if session.get('user_type') != 'admin':
        return redirect(url_for('login'))

    patient = Patient.query.get_or_404(patient_id)
    all_appointments = (
        Appointment.query
        .filter_by(patient_id=patient_id)
        .order_by(Appointment.appointment_date.desc())
        .all()
    )

    return render_template(
        "patient_history.html",
        this_user=patient,
        all_appointments=all_appointments,
        back_url=url_for('admin'),
    )

@app.route("/patient_history_from_dr_dash/<int:patient_id>")
def patient_history_from_dr_dash(patient_id):
     this_user_id = session.get('user_id')
     if this_user_id is None or session.get('user_type') != 'doctor':
        return redirect(url_for('login'))
     patient = Patient.query.get_or_404(patient_id)
     all_appointments = (
        Appointment.query
        .filter_by(patient_id=patient_id)
        .order_by(Appointment.appointment_date.desc())
        .all()
     )
     
     return render_template( "patient_history.html", back_url=url_for('doctor_dashboard', doctor_id=this_user_id),
        this_user=patient,
        all_appointments=all_appointments,)  # Replace with your appointments endpoint



@app.route("/back_btn_admin")
def back_btn_admin():
    return render_template("admin_dashboard.html")

@app.route("/update_patients_history/<int:appointment_id>", methods=["GET", "POST"])
def update_patient_history(appointment_id):
    if session.get('user_type') != 'doctor':
        return redirect(url_for('login'))

    appt = Appointment.query.get_or_404(appointment_id)
    treatment = appt.treatment  

    if request.method == "POST":
        visit_type = request.form.get("visit_type")
        tests_done = request.form.get("test_done")
        diagnosis = request.form.get("diagnosis")
        prescription = request.form.get("prescription")

      
        med1 = request.form.get("med1")
        med2 = request.form.get("med2")
        med3 = request.form.get("med3")
        medicines = ", ".join([m for m in [med1, med2, med3] if m])

        if treatment is None:
            treatment = Treatment(
                appointment_id=appointment_id,
                visit_type=visit_type,
                tests_done=tests_done,
                diagnosis=diagnosis,
                prescription=prescription,
                medicines=medicines,
            )
            db.session.add(treatment)
        else:
            treatment.visit_type = visit_type
            treatment.tests_done = tests_done
            treatment.diagnosis = diagnosis
            treatment.prescription = prescription
            treatment.medicines = medicines

        db.session.commit()
        return redirect(url_for("doctor_dashboard", doctor_id=appt.doctor_id))

    return render_template(
        "update_patients_history.html",
        appointment=appt,
        treatment=treatment,
    )
from datetime import date, timedelta

from datetime import date, timedelta

@app.route("/doctor_availability", methods=["GET", "POST"])
def doctor_availability():
    if session.get('user_type') != 'doctor':
        return redirect(url_for('login'))

    doctor_id = session.get('user_id')

    if request.method == "POST":
        Availability.query.filter_by(doctor_id=doctor_id).delete()

        for i in range(7):
            d_str = request.form.get(f"date_{i}")
            if not d_str:
                continue
            d = date.fromisoformat(d_str)
            m = request.form.get(f"morning_{i}") == "on"
            e = request.form.get(f"evening_{i}") == "on"
            if m or e:
                db.session.add(Availability(
                    doctor_id=doctor_id,
                    date=d,
                    morning_available=m,
                    evening_available=e
                ))
        db.session.commit()
        return redirect(url_for("doctor_dashboard", doctor_id=doctor_id))

    today = date.today()
    days = [today + timedelta(days=i) for i in range(7)]
    existing = Availability.query.filter_by(doctor_id=doctor_id).all()
    by_date = {a.date: a for a in existing}

    return render_template("doctor_availability.html",
                           days=days,
                           availability_by_date=by_date)

@app.route("/dr_avail")
def dr_avail():
    return render_template("dr-avail.html")

@app.route("/department/<int:dept_id>")
def department_detail(dept_id):
   
    department = Department.query.get_or_404(dept_id)
    doctors = department.doctors
   
    return render_template(
        "view_details.html",
        department=department,
        doctors=doctors,
        back_url=url_for('patient', patient_id=session.get('user_id'))
    )


@app.route("/dr_detail_card/<int:doctor_id>/<int:dept_id>")
def dr_detail_card(doctor_id, dept_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    return render_template(
        "dr_detail_card.html",
        doctor=doctor,
        back_url=url_for('department_detail', dept_id=dept_id)
    )

@app.route("/appointment/<int:appointment_id>/complete", methods=["POST"])
def complete_appointment(appointment_id):
    print("HIT complete_appointment:", appointment_id)

    if session.get('user_type') != 'doctor':
        print(" -> not doctor, redirecting")
        return redirect(url_for('login'))

    appt = Appointment.query.get_or_404(appointment_id)
    print(" -> appt doctor_id:", appt.doctor_id, "session doctor_id:", session.get('user_id'))

    if appt.doctor_id != session.get('user_id'):
        print(" -> doctor mismatch, NOT updating")
        return redirect(url_for('login'))

    appt.status = "Completed"
    db.session.commit()
    print(" -> saved status to:", appt.status)

    return redirect(url_for("doctor_dashboard", doctor_id=appt.doctor_id))


@app.route("/appointment/<int:appointment_id>/cancel", methods=["POST"])
def cancel_appointment(appointment_id):
    if session.get('user_type') != 'doctor':
        return redirect(url_for('login'))

    appt = Appointment.query.get_or_404(appointment_id)
    if appt.doctor_id != session.get('user_id'):
        return redirect(url_for('login'))

    appt.status = "Cancelled"
    db.session.commit()
    return redirect(url_for("doctor_dashboard", doctor_id=appt.doctor_id))

@app.route("/patient/appointment/<int:appointment_id>/cancel", methods=["POST"])
def patient_cancel_appointment(appointment_id):
    if session.get('user_type') != 'patient':
        return redirect(url_for('login'))

    patient_id = session.get('user_id')
    appt = Appointment.query.get_or_404(appointment_id)

    if appt.patient_id != patient_id:
        return redirect(url_for('login'))

    appt.status = "Cancelled"
    db.session.commit()
    return redirect(url_for('patient', patient_id=patient_id))


@app.route("/patient/profile/edit", methods=["GET", "POST"])
def edit_profile():
    if session.get('user_type') != 'patient':
        return redirect(url_for('login'))

    patient_id = session.get('user_id')
    patient = Patient.query.get_or_404(patient_id)

    if request.method == "POST":
        full_name = request.form.get("full_name")
        contact = request.form.get("contact")

        if not full_name or not contact:
            flash("Please fill in all fields.", "error")
            return redirect(url_for('edit_profile'))

        
        existing = Patient.query.filter(
            Patient.contact == contact,
            Patient.id != patient_id
        ).first()
        if existing:
            flash("This contact number is already used by another patient.", "error")
            return redirect(url_for('edit_profile'))

        patient.full_name = full_name
        patient.contact = contact
        db.session.commit()
        flash("Profile updated successfully.", "success")
        return redirect(url_for('patient', patient_id=patient_id))
    return render_template("edit_profile.html", patient=patient)

from sqlalchemy import or_

@app.route("/search")
def search():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    q = request.args.get("q", "").strip()
    if not q:
       
        patient_id = session.get('user_id')
        return redirect(url_for('patient', patient_id=patient_id))

   
    dept = Department.query.filter(Department.name.ilike(q)).first()
    if dept:
        return redirect(url_for('department_detail', dept_id=dept.id))

    
    doctor = Doctor.query.filter(Doctor.full_name.ilike(q)).first()
    if doctor:
        return redirect(url_for('dr_detail_card',
                                doctor_id=doctor.id,
                                dept_id=doctor.specialization))

   
    patient_match = (
        Patient.query.filter(
            or_(
                Patient.full_name.ilike(q),
                Patient.username.ilike(q)
            )
        ).first()
    )
    if patient_match:
       
        return redirect(
            url_for('patient_history_from_appointments', patient_id=patient_match.id)
        )

   
    patient_id = session.get('user_id')
    flash("No exact match found for your search.", "error")
    return redirect(url_for('patient', patient_id=patient_id))

@app.route("/admin/doctor/<int:doctor_id>/edit", methods=["GET", "POST"])
def admin_edit_doctor(doctor_id):
    if session.get('user_type') != 'admin':
        return redirect(url_for('login'))

    doctor = Doctor.query.get_or_404(doctor_id)

    if request.method == "POST":
        doctor.full_name = request.form.get("full_name")
        doctor.experience = int(request.form.get("experience") or doctor.experience)
        db.session.commit()
        return redirect(url_for('admin'))

    return render_template("admin_edit_doctor.html", doctor=doctor)


@app.route("/admin/doctor/<int:doctor_id>/cancel_future", methods=["POST"])
def admin_cancel_doctor_future(doctor_id):
    if session.get('user_type') != 'admin':
        return redirect(url_for('login'))

    today = date.today()
    future = (Appointment.query
              .filter_by(doctor_id=doctor_id, status="Scheduled")
              .filter(Appointment.appointment_date >= today)
              .all())
    for appt in future:
        appt.status = "Cancelled"
    db.session.commit()
    flash("Appointment has been cancelled.", "success")
    return redirect(url_for('admin'))


@app.route("/admin/doctor/<int:doctor_id>/blacklist", methods=["POST"])
def admin_blacklist_doctor(doctor_id):
    if session.get('user_type') != 'admin':
        return redirect(url_for('login'))

    doctor = Doctor.query.get_or_404(doctor_id)
    doctor.is_active = False
    db.session.commit()
    return redirect(url_for('admin'))

@app.route("/admin/patient/<int:patient_id>/edit", methods=["GET", "POST"])
def admin_edit_patient(patient_id):
    if session.get('user_type') != 'admin':
        return redirect(url_for('login'))

    patient = Patient.query.get_or_404(patient_id)

    if request.method == "POST":
        patient.full_name = request.form.get("full_name")
        patient.contact = request.form.get("contact")
        db.session.commit()
        return redirect(url_for('admin'))

    return render_template("admin_edit_patient.html", patient=patient)


@app.route("/admin/patient/<int:patient_id>/cancel_future", methods=["POST"])
def admin_cancel_patient_future(patient_id):
    if session.get('user_type') != 'admin':
        return redirect(url_for('login'))

    today = date.today()
    future = (Appointment.query
              .filter_by(patient_id=patient_id, status="Scheduled")
              .filter(Appointment.appointment_date >= today)
              .all())
    for appt in future:
        appt.status = "Cancelled"
    db.session.commit()
    flash("Appointment has been cancelled.", "success")
    return redirect(url_for('admin'))


@app.route("/admin/patient/<int:patient_id>/blacklist", methods=["POST"])
def admin_blacklist_patient(patient_id):
    if session.get('user_type') != 'admin':
        return redirect(url_for('login'))

    patient = Patient.query.get_or_404(patient_id)
    patient.is_active = False
    db.session.commit()
    return redirect(url_for('admin'))

from flask import Flask, render_template, url_for, redirect, request
from flask import current_app as app
from .models import *
 
@app.route("/")
def home():
    return render_template("index.html", active="home")

@app.route("/login", methods=['GET', 'POST'])
def login():
     if request.method == 'POST':
        username= request.form['username']
        password= request.form.get('password')
        
        this_user = Admin.query.filter_by(username=username).first()
        if not this_user:
            # Check Doctor
            this_user = Doctor.query.filter_by(username=username).first()
        if not this_user:
            # Check Patient
            this_user = Patient.query.filter_by(username=username).first()

        if this_user:
            if this_user.password== password:
                if this_user.type=="admin":
                    return redirect(url_for('admin'))
                elif this_user.type=="doctor":
                    return redirect(url_for('doctor_dashboard'))
                elif this_user.type=="patient":
                    return redirect(url_for('patient'))
            else:
                return render_template("incorrect_password.html")
        else:
            return render_template("user_not_found.html")
        
     return render_template("login.html", active="login")

@app.route("/register", methods=['GET', 'POST'])
def register() :
    if request.method == 'POST':
        username= request.form['username']
        password= request.form.get('password')
        contact= request.form.get('contact')
        user_name = Patient.query.filter_by(username=username).first()
        user_contact = Patient.query.filter_by(contact=contact).first()
        if user_name or user_contact:
            return render_template("already_registered.html", error="Username already exists!")

        # Create Patient object
        new_patient = Patient(
            username=username,
            password=password,
            contact= contact,
            type="patient"
        )

        db.session.add(new_patient)
        db.session.commit()

        return redirect(url_for('login'))    
    return render_template("register.html", active="register")

@app.route("/admin")
def admin():
    return render_template("admin_dashboard.html")

@app.route("/patient")
def patient():
    return render_template("patient_dashboard.html")

@app.route("/doctor_dashboard")
def doctor_dashboard():
    return render_template("doctor_dashboard.html")

@app.route("/add_doctor")
def add_doctor():
    return render_template("add_doctor.html")

@app.route("/patient_history_from_dashboard")
def patient_history_from_dashboard():
    return render_template("patient_history.html", back_url=url_for('patient'))

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


    
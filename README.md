# 🏥 Hospital Management System (HMS)

A full-stack Flask-based web application designed to efficiently manage hospital operations including patients, doctors, appointments, and treatment records with role-based access control.

---

## 🚀 Key Features

- 🔐 Role-based authentication (Admin, Doctor, Patient)
- 📅 Smart appointment booking with conflict prevention
- 👨‍⚕️ Doctor availability management (7-day schedule)
- 📋 Patient treatment history and medical records
- 🏥 Department-based doctor categorization
- 🔎 Search functionality (Doctor, Patient, Department)
- 🚫 Soft blacklist system for user control
- 📊 Admin dashboard for system monitoring

---

## 🛠️ Tech Stack

- **Backend:** Flask (Python)
- **Database:** SQLite (SQLAlchemy ORM)
- **Frontend:** HTML, CSS, Bootstrap, JavaScript
- **Authentication:** Flask-Login
- **Forms:** WTForms

---

## 🧠 System Design & Architecture

### 📌 Architecture Overview
- `app.py` → Application entry point
- `models.py` → Database schema (SQLAlchemy)
- `controllers.py` → Business logic & routing
- `templates/` → Jinja2 HTML templates
- `static/` → CSS, images

---

## 🗄️ Database Schema

### Entities:
- Admin
- Doctor
- Patient
- Department
- Appointment
- Treatment
- Availability

### Relationships:
- One-to-Many → Department → Doctor  
- One-to-Many → Doctor → Appointment  
- One-to-Many → Patient → Appointment  
- One-to-One → Appointment → Treatment  
- One-to-Many → Doctor → Availability  

---

## ⚙️ Core Functionalities

### 👤 Admin
- Add/Edit doctors and patients
- Blacklist users
- View system-wide data

### 👨‍⚕️ Doctor
- Manage availability
- View appointments
- Update treatment records

### 🧑‍🤝‍🧑 Patient
- Register/Login
- Book appointments
- View medical history

---

## 🔗 API Endpoints (Sample)

| Endpoint | Method | Description |
|----------|--------|------------|
| /login | GET, POST | User authentication |
| /register | GET, POST | Patient registration |
| /book/<doctor_id> | GET, POST | Book appointment |
| /doctor_availability | GET, POST | Set availability |
| /appointment/<id>/complete | POST | Mark completed |

---

## 🧠 Key Concepts Implemented

- Database Normalization
- Role-Based Access Control (RBAC)
- RESTful Routing
- Session Management
- Conflict-free Scheduling Logic

---

## ▶️ How to Run

```bash
git clone https://github.com/your-username/hospital-management-system.git
cd hospital-management-system

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

python app.py
```


---

## 📈 Future Improvements

- FastAPI-based microservices
- Cloud deployment (AWS)
- Real-time notifications
- Better UI/UX

---
## 📷 Application Screenshots

### 🏠 Landing Page
![Landing Page](https://github.com/user-attachments/assets/3826eaa2-1ff8-420c-b3b2-6ae5ccc49dab)

---

### 🔐 Login Page
![Login Page](https://github.com/user-attachments/assets/9d4a73c6-c396-475e-8fa8-78ed36e2943d)

---

### 🛠️ Admin Dashboard
![Admin Dashboard](https://github.com/user-attachments/assets/0d9fc330-c732-42ca-96ea-8d8be4a5467c)

*Admin can manage doctors, patients, and monitor overall system activity.*

---

### 👩‍⚕️ Doctor Details
![Doctor Availability](https://github.com/user-attachments/assets/be106a12-14c5-4e32-8b8e-9d6991807766)

---

### 🧑‍🤝‍🧑 Patient Dashboard
![Patient Dashboard](https://github.com/user-attachments/assets/6b75d977-7124-4128-9109-7dfe733d2faf)

---

### 📋 Doctor Availability Management
![Appointments](https://github.com/user-attachments/assets/6e3bab2d-27f9-4fc8-b1c0-09a42ee25016)

---


# Hospital Management Application

This is a Flask-based web application designed to manage hospital operations, including patient records, doctor information, appointments, and department management. It features distinct interfaces for administrators, doctors, and patients, providing a comprehensive solution for hospital management.

## Features

*   **User Authentication:** Secure login for Admin, Doctor, and Patient roles.
*   **Admin Dashboard:**
    *   Manage doctors (add, edit, delete).
    *   Manage departments (add, edit, delete).
    *   View all patients.
*   **Doctor Dashboard:**
    *   View assigned patients.
    *   Update patient medical history.
    *   Manage availability.
*   **Patient Dashboard:**
    *   Register and create a profile.
    *   View personal medical history.
    *   Book and view appointments.
    *   Check doctor availability.
*   **Database Management:** Uses SQLite for data storage with SQLAlchemy ORM.

## Technologies Used

*   **Backend:** Python, Flask
*   **Database:** SQLite, Flask-SQLAlchemy
*   **Frontend:** HTML, CSS

## Setup and Installation

To get this project up and running on your local machine, follow these steps:

### 1. Clone the Repository
```bash
git clone https://github.com/23f2003543/hospital-management-app-v1.git
cd hospital-management-app-v1
```

### 2. Create a Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python app.py
```

The application will be accessible at http://127.0.0.1:5000/.

## Default Credentials
For initial testing, the following default credentials are provided:
* Admin:
    * Username: `admin`
    * Password: `admin`

## Project Structure
```bash
.
├── .gitignore
├── app.py                      # Main Flask application file
├── HMS_report.pdf              # Project report/documentation
├── README.md                   # Project README file
├── requirements.txt            # Python dependencies
├── application/
│   ├── __init__.py
│   ├── controllers.py          # Route definitions and logic
│   ├── database.py             # Database initialization
│   └── models.py               # SQLAlchemy models
├── instance/
│   └── hospital.db             # SQLite database file
├── static/
│   ├── home_icon.png           # Static images
│   ├── style.css               # Global stylesheets
│   └── style1.css
└── templates/
    ├── admin_dashboard.html    # HTML templates for various pages
    ├── admin_login.html
    ├── base.html
    ├── check_availability.html
    ├── doc_login.html
    ├── doctor_availability.html
    ├── doctor_dashboard.html
    ├── doctor_details.html
    ├── doctor_register.html
    ├── edit_doctor.html
    ├── edit_patient.html
    ├── home.html
    ├── patient_dashboard.html
    ├── patient_login.html
    ├── patient_profile.html
    ├── patient_register.html
    └── update_patient_history.html
    └── view_appointment.html
    └── view_departments.html
```
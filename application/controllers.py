from flask import Flask, render_template, request, redirect, flash, session, url_for
from flask import current_app as app
from .models import *

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html")

@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    flash("Looged out Successfully", "success")
    return redirect(url_for("home"))

@app.route("/history", methods=["GET", "POST"])
def history():
    return "patient history"

@app.route("/patient_profile", methods=["GET", "POST"])
def patient_profile():
    return "patient profile edit here"

@app.route("/base", methods=["GET", "POST"])
def base():
    return render_template('base.html')

@app.route("/patient_register", methods=["GET", "POST"])
def patient_register():
    if request.method == "POST":
        email = request.form.get('email')
        username = request.form.get('username')
        name = request.form.get('username')
        password = request.form.get('password')
        user = Patient.query.filter_by(username=username, email=email, password=password).first()
        if user:
            print("user exist")
            flash("User already exist with this credentials", "error")
            return redirect('patient_login')
        new_user=Patient(username=username, email=email, password=password, name=name)
        flash("Patient registered login with your username and password", "successfull")
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('patient_login'))

    return render_template("patient_register.html")

@app.route("/patient_login", methods=["GET", "POST"])
def patient_login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        user = Patient.query.filter_by(username=username, password=password).first()
        if not user:
            print("user not exist")
            flash("User does not exist or invalid credentials", "error")
            return redirect('patient_login')
        
        session['username'] = user.username
        session['user_type'] = 'patient'
        return redirect('patient_dashboard')
    return render_template('patient_login.html')

@app.route("/doctor_login", methods=["GET", "POST"])
def doc_login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        user = Doctor.query.filter_by(username=username, password=password).first()
        if not user:
            print("user not exist")
            flash("User does not exist or invalid credentials", "error")
            return redirect('doc_login')
        
        session['username'] = user.username
        session['user_type'] = 'doctor'
        return redirect('doctor_dashboard')
    return render_template('doc_login.html')

@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        user = Admin.query.filter_by(username=username, password=password).first()
        if not user:
            print("user not exist")
            flash("User does not exist or invalid credentials", "error")
            return redirect('admin_login')
        
        session['username'] = user.username
        session['user_type'] = 'admin'
        return redirect('admin_dashboard')
    return render_template('admin_login.html')

@app.route("/patient_dashboard", methods=["GET", "POST"])
def patient_dashboard():
    return render_template('patient_dashboard.html')

@app.route("/doctor_dashboard", methods=["GET", "POST"])
def doctor_dashboard():
    return render_template('doctor_dashboard.html')

@app.route("/admin_dashboard", methods=["GET", "POST"])
def admin_dashboard():
    if session.get('user_type') != 'admin':
        flash('Access denied.', 'error')
        return redirect(url_for('home'))

    query = request.args.get('q', '').strip()

    # start with query objects
    doctors_q = Doctor.query
    patients_q = Patient.query
    appointments_q = Appointment.query.join(Patient).join(Doctor)

    if query:
        search = f"%{query}%"
        doctors = doctors_q.filter(Doctor.name.ilike(search)).all()
        patients = patients_q.filter(Patient.name.ilike(search)).all()
        appointments = appointments_q.filter(
            Patient.name.ilike(search) | Doctor.name.ilike(search)
        ).all()
    else:
        doctors = doctors_q.all()
        patients = patients_q.all()
        appointments = appointments_q.all()

    appointments_with_details = []
    for appt in appointments:
        appointments_with_details.append({
            'id': appt.id,
            'patient': appt.patient,   # use backref provided objects
            'doctor': appt.doctor,
            'date': appt.date,
            'time': appt.time,
            'status': appt.status
        })

    return render_template('admin_dashboard.html', doctors=doctors, patients=patients, appointments=appointments_with_details)

@app.route("/doctor_register", methods=["GET", "POST"])
def doctor_register():
    if session.get('user_type') != 'admin':
        flash('Unauthorized access.', 'error')
        return redirect(url_for('home'))
    
    departments = Department.query.all()
    if request.method == 'POST':
        doctor = Doctor(
            name=request.form['name'],
            email=request.form['email'],
            username=request.form['username'],
            password=request.form['password'],
            Dep_id=int(request.form['Dep_id']),
            gender=request.form['gender']
        )
        db.session.add(doctor)
        db.session.commit()
        flash(f'Doctor {doctor.name} registered successfully!', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('doctor_register.html', departments=departments)

@app.route('/edit_doctor/<int:doctor_id>', methods=["GET", "POST"])
def edit_doctor(doctor_id):
    if session.get('user_type') != 'admin':
        flash('Access denied.', 'error')
        return redirect(url_for('home'))
    doctor = Doctor.query.get_or_404(doctor_id)
    departments = Department.query.all()
    if request.method == 'POST':
        doctor.name = request.form['name']
        doctor.email = request.form['email']
        doctor.username = request.form['username']
        doctor.Dep_id = int(request.form['Dep_id'])
        doctor.gender = request.form['gender']
        db.session.commit()
        flash(f'Dr. {doctor.name} updated successfully!', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('edit_doctor.html', doctor=doctor, departments=departments)

@app.route('/edit_patient/<int:patient_id>', methods=["GET", "POST"])
def edit_patient(patient_id):
    if session.get('user_type') != 'admin':
        flash('Access denied.', 'error')
        return redirect(url_for('home'))
    patient = Patient.query.get_or_404(patient_id)
    if request.method == "POST":
        patient.name = request.form['name']
        patient.email = request.form['email']
        patient.username = request.form['username']
        patient.age = int(request.form['age'])
        patient.gender = request.form['gender']
        db.session.commit()
        flash(f'{patient.name} updated successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('edit_patient.html', patient=patient)

@app.route('/delete_doctor/<int:doctor_id>')
def delete_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    db.session.delete(doctor)
    db.session.commit()
    flash(f'Dr. {doctor.name} deleted.', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/delete_patient/<int:patient_id>')
def delete_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    db.session.delete(patient)
    db.session.commit()
    flash(f' {patient.name} deleted.', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/blacklist_patient/<int:patient_id>')
def blacklist_patient(patient_id):
    # Add logic: maybe set is_blacklisted = True
    flash('Patient blacklisted.', 'warning')
    return redirect(url_for('admin_dashboard'))

@app.route('/blacklist_doctor/<int:doctor_id>')
def blacklist_doctor(doctor_id):
    # Add logic: maybe set is_blacklisted = True
    flash('Doctor blacklisted.', 'warning')
    return redirect(url_for('admin_dashboard'))

@app.route('/view_appointment/<int:appt_id>')
def view_appointment(appt_id):
    appointment = Appointment.query.get_or_404(appt_id)

    # Query treatments for the same patient-doctor pair, only for completed appointments
    treatments = Treatment.query.join(Appointment, Treatment.appoint_id == Appointment.id).filter(
        Appointment.p_id == appointment.p_id,
        Appointment.d_id == appointment.d_id,
        Appointment.status == 'Completed'
    ).order_by(Appointment.date).all()

    return render_template(
        'view_appointment.html',
        patient=appointment.patient,
        doctor=appointment.doctor,
        treatments=treatments
    )
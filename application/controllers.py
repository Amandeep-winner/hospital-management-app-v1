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

@app.route("/history/<int:patient_id>", methods=["GET", "POST"])
def history(patient_id):
    if session.get('user_type') != 'patient':
        flash('Access denied.', 'error')
        return redirect(url_for('logout'))

    if patient_id != session.get('user_id'):
        flash('Access denied.', 'error')
        return redirect(url_for('patient_dashboard'))

    current_patient = Patient.query.get_or_404(patient_id)

    doctors = db.session.query(Doctor).join(Appointment).filter(
        Appointment.p_id == current_patient.id,
        Appointment.status == 'Completed'
    ).distinct().all()

    treatments = Treatment.query.join(Appointment, Treatment.appoint_id == Appointment.id).filter(
        Appointment.p_id == current_patient.id,
        Appointment.status == 'Completed'
    ).order_by(Appointment.date).all()

    return render_template('patient_profile.html', patient=current_patient, doctors=doctors, treatments=treatments)

@app.route('/patient_profile/<int:patient_id>', methods=["GET", "POST"])
def patient_profile(patient_id):
    if session.get('user_type') != 'patient':
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
        return redirect(url_for('patient_dashboard'))
    return render_template('edit_patient.html', patient=patient)

@app.route('/cancel_appointment_patient/<int:appt_id>', methods=['POST'])
def cancel_appointment_patient(appt_id):
    appt = Appointment.query.get_or_404(appt_id)
    if appt.patient.id != session['user_id']:
        flash('Unauthorized', 'error')
        return redirect(url_for('patient_dashboard'))
    
    appt.status = 'Cancelled'
    db.session.commit()
    flash('Appointment cancelled.', 'warning')
    return redirect(url_for('patient_dashboard'))

@app.route('/view_department/<int:dep_id>', methods=["GET", "POST"])
def view_department(dep_id):
    if session.get('user_type') != 'patient':
        flash('Access denied.', 'error')
        return redirect(url_for('home'))

    department = Department.query.get_or_404(dep_id)
    doctors = Doctor.query.filter_by(Dep_id=dep_id).all()

    return render_template(
        'view_departments.html',
        department=department,
        doctors=doctors
    )


@app.route('/check_availability/<int:doctor_id>')
def check_availability(doctor_id):
    from datetime import date, timedelta
    if session.get('user_type') != 'patient':
        flash('Access denied.', 'error')
        return redirect(url_for('home'))

    doctor = Doctor.query.get_or_404(doctor_id)
    today = date.today()
    availability = []

    for i in range(7):
        day_date = today + timedelta(days=i)
        avail = DoctorAvailability.query.filter_by(doctor_id=doctor.id, date=day_date).first()
        morning_booked = Appointment.query.filter_by(
            d_id=doctor.id,
            date=day_date,
            time='10:00:00',
            status='Booked'
        ).first() is not None

        evening_booked = Appointment.query.filter_by(
            d_id=doctor.id,
            date=day_date,
            time='18:00:00',
            status='Booked'
        ).first() is not None

        availability.append({
            'date': day_date,
            'morning_available': avail.morning_slot if avail else False,
            'evening_available': avail.evening_slot if avail else False,
            'morning_booked': morning_booked,
            'evening_booked': evening_booked
        })

    return render_template('check_availability.html', doctor=doctor, availability=availability)

@app.route('/doctor_details/<int:doctor_id>')
def doctor_details(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    return render_template('doctor_details.html', doctor=doctor)


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

        if user.is_blacklisted:
            flash('Your account has been suspended. Contact admin.', 'error')
            return redirect(url_for('home'))
        
        session['user_id'] = user.id
        session['username'] = user.username
        session['user_type'] = 'patient'
        return redirect('patient_dashboard')
    return render_template('patient_login.html')

@app.route("/doctor_login", methods=["GET", "POST"])
def doctor_login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        user = Doctor.query.filter_by(username=username, password=password).first()
        if not user:
            print("user not exist")
            flash("User does not exist or invalid credentials", "error")
            return redirect(url_for('doctor_login'))
    
        if user.is_blacklisted:
            flash('Your account has been suspended. Contact admin.', 'error')
            return redirect(url_for('home'))
        session['user_id'] = user.id
        session['username'] = user.username
        session['user_type'] = 'doctor'
        return redirect(url_for('doctor_dashboard'))
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
        
        session['user_id'] = user.id
        session['username'] = user.username
        session['user_type'] = 'admin'
        return redirect('admin_dashboard')
    return render_template('admin_login.html')

@app.route("/patient_dashboard", methods=["GET", "POST"])
def patient_dashboard():
    if session.get('user_type') != 'patient':
        flash('Access denied.', 'error')
        return redirect(url_for('home'))
    
    current_patient = Patient.query.get(session.get('user_id'))
    if not current_patient:
        flash('Session expired.', 'error')
        return redirect(url_for('patient_login'))
    
    departments = Department.query.all()

    from datetime import date, datetime
    today = date.today()
    upcoming_appointments = Appointment.query.filter(
        Appointment.p_id == current_patient.id,
        Appointment.date >= today,
        Appointment.status == 'Booked'
    ).order_by(Appointment.date, Appointment.time).all()

    return render_template(
        'patient_dashboard.html',
        current_patient=current_patient,
        departments=departments,
        upcoming_appointments=upcoming_appointments
    )


@app.route("/admin_dashboard", methods=["GET", "POST"])
def admin_dashboard():
    if session.get('user_type') != 'admin':
        flash('Access denied.', 'error')
        return redirect(url_for('home'))

    query = request.args.get('q', '').strip()

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
            'patient': appt.patient,
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
    if session.get('user_type') != 'admin':
        flash('Access denied.', 'error')
        return redirect(url_for('home'))
    doctor = Doctor.query.get_or_404(doctor_id)
    appointments = Appointment.query.filter_by(d_id=doctor_id).all()
    for appointment in appointments:
        treatments = Treatment.query.filter_by(appoint_id=appointment.id).all()
        for treatment in treatments:
            Medicine.query.filter_by(treatment_id=treatment.id).delete()
            db.session.delete(treatment)
        db.session.delete(appointment)
    DoctorAvailability.query.filter_by(doctor_id=doctor_id).delete()
    db.session.delete(doctor)
    db.session.commit()
    flash(f'Dr. {doctor.name} and all associated records deleted.', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/delete_patient/<int:patient_id>')
def delete_patient(patient_id):
    if session.get('user_type') != 'admin':
        flash('Access denied.', 'error')
        return redirect(url_for('home'))
    patient = Patient.query.get_or_404(patient_id)
    appointments = Appointment.query.filter_by(p_id=patient_id).all()
    for appointment in appointments:
        treatments = Treatment.query.filter_by(appoint_id=appointment.id).all()
        for treatment in treatments:
            Medicine.query.filter_by(treatment_id=treatment.id).delete()
            db.session.delete(treatment)
        db.session.delete(appointment)
    db.session.delete(patient)
    db.session.commit()
    flash(f'{patient.name} and all associated records deleted.', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/blacklist_doctor/<int:doctor_id>')
def blacklist_doctor(doctor_id):
    if session.get('user_type') != 'admin':
        flash('Access denied.', 'error')
        return redirect(url_for('home'))
    doctor = Doctor.query.get_or_404(doctor_id)
    doctor.is_blacklisted = True
    db.session.commit()
    flash(f'Dr. {doctor.name} has been blacklisted.', 'warning')
    return redirect(url_for('admin_dashboard'))

@app.route('/unblacklist_doctor/<int:doctor_id>')
def unblacklist_doctor(doctor_id):
    if session.get('user_type') != 'admin':
        flash('Access denied.', 'error')
        return redirect(url_for('home'))
    
    doctor = Doctor.query.get_or_404(doctor_id)
    doctor.is_blacklisted = False
    db.session.commit()
    flash(f'Dr. {doctor.name} has been removed from blacklist.', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/blacklist_patient/<int:patient_id>')
def blacklist_patient(patient_id):
    if session.get('user_type') != 'admin':
        flash('Access denied.', 'error')
        return redirect(url_for('home'))
    
    patient = Patient.query.get_or_404(patient_id)
    patient.is_blacklisted = True
    db.session.commit()
    flash(f'{patient.name} has been blacklisted.', 'warning')
    return redirect(url_for('admin_dashboard'))

@app.route('/unblacklist_patient/<int:patient_id>')
def unblacklist_patient(patient_id):
    if session.get('user_type') != 'admin':
        flash('Access denied.', 'error')
        return redirect(url_for('home'))
    
    patient = Patient.query.get_or_404(patient_id)
    patient.is_blacklisted = False
    db.session.commit()
    flash(f'{patient.name} has been removed from blacklist.', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/view_appointment/<int:appt_id>')
def view_appointment(appt_id):
    appointment = Appointment.query.get_or_404(appt_id)

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

@app.route('/view_patient_history/<int:patient_id>')
def view_patient_history(patient_id):
    if session.get('user_type') != 'doctor':
        flash('Access denied.', 'error')
        return redirect(url_for('home'))

    current_doctor = Doctor.query.get(session['user_id'])
    patient = Patient.query.get_or_404(patient_id)

    treatments = Treatment.query.join(Appointment, Treatment.appoint_id == Appointment.id).filter(
        Appointment.p_id == patient.id,
        Appointment.d_id == current_doctor.id,
        Appointment.status == 'Completed'
    ).order_by(Appointment.date).all()

    return render_template('view_appointment.html', patient=patient, doctor=current_doctor, treatments=treatments)

# docotor
@app.route('/doctor_dashboard')
def doctor_dashboard():
    if session.get('user_type') != 'doctor':
        flash('Access denied. Doctors only.', 'error')
        return redirect(url_for('home'))

    current_doctor = Doctor.query.get(session['user_id'])

    from datetime import date, datetime
    today = date.today()

    upcoming_appointments = Appointment.query.filter(
        Appointment.d_id == current_doctor.id,
        Appointment.date >= today,
        Appointment.status == 'Booked'
    ).order_by(Appointment.date, Appointment.time).all()

    all_patients = db.session.query(Patient).join(Appointment).filter(
        Appointment.d_id == current_doctor.id,
        Appointment.status == 'Completed'
    ).distinct().all()

    return render_template(
        'doctor_dashboard.html',
        upcoming_appointments=upcoming_appointments,
        all_patients=all_patients
    )

@app.route('/complete_appointment/<int:appt_id>', methods=['POST'])
def complete_appointment(appt_id):
    appt = Appointment.query.get_or_404(appt_id)
    if appt.doctor.id != session['user_id']:
        flash('Unauthorized', 'error')
        return redirect(url_for('doctor_dashboard'))
    
    appt.status = 'Completed'
    db.session.commit()
    flash('Appointment marked as complete!', 'success')
    return redirect(url_for('doctor_dashboard'))


@app.route('/cancel_appointment/<int:appt_id>', methods=['POST'])
def cancel_appointment(appt_id):
    appt = Appointment.query.get_or_404(appt_id)
    if appt.doctor.id != session['user_id']:
        flash('Unauthorized', 'error')
        return redirect(url_for('doctor_dashboard'))
    
    appt.status = 'Cancelled'
    db.session.commit()
    flash('Appointment cancelled.', 'warning')
    return redirect(url_for('doctor_dashboard'))

@app.route('/update_patient_history/<int:appt_id>', methods=['GET', 'POST'])
def update_patient_history(appt_id):
    if session.get('user_type') != 'doctor':
        flash('Access denied.', 'error')
        return redirect(url_for('home'))

    appointment = Appointment.query.get_or_404(appt_id)
    if appointment.d_id != session['user_id']:
        flash('Unauthorized', 'error')
        return redirect(url_for('doctor_dashboard'))

    if request.method == 'POST':
        treatment = Treatment(
            appoint_id=appointment.id,
            diagnosis=request.form['diagnosis'],
            prescription=request.form['prescription'],
            notes=request.form.get('tests_done') + " | Visit: " + request.form.get('visit_type', 'In-person')
        )
        db.session.add(treatment)

        names = request.form.getlist('medicine_name')
        dosages = request.form.getlist('medicine_dosage')
        for name, dosage in zip(names, dosages):
            if name.strip():
                med = Medicine(
                    treatment=treatment,
                    name=name.strip(),
                    dosage=dosage.strip()
                )
                db.session.add(med)

        appointment.status = 'Completed'
        db.session.commit()

        flash('Patient history updated successfully!', 'success')
        return redirect(url_for('doctor_dashboard'))

    return render_template(
        'update_patient_history.html',
        appointment=appointment,
        patient=appointment.patient,
        doctor=appointment.doctor
    )


from datetime import date, timedelta

@app.route('/doctor_availability', methods=['GET', 'POST'])
def doctor_availability():
    if session.get('user_type') != 'doctor':
        flash('Access denied.', 'error')
        return redirect(url_for('home'))

    doctor = Doctor.query.get(session['user_id'])
    today = date.today()
    next_7_days = []

    for i in range(7):
        current_date = today + timedelta(days=i)
        avail = DoctorAvailability.query.filter_by(
            doctor_id=doctor.id, 
            date=current_date
        ).first()

        next_7_days.append({
            'date': current_date,
            'morning': avail.morning_slot if avail else False,
            'evening': avail.evening_slot if avail else False
        })

    if request.method == 'POST':
        
        DoctorAvailability.query.filter(
            DoctorAvailability.doctor_id == doctor.id,
            DoctorAvailability.date >= today,
            DoctorAvailability.date < today + timedelta(days=7)
        ).delete()

        for i in range(7):
            day_date = today + timedelta(days=i)
            morning_key = f"available_{day_date.strftime('%Y%m%d')}_morning"
            evening_key = f"available_{day_date.strftime('%Y%m%d')}_evening"

            morning = morning_key in request.form
            evening = evening_key in request.form

            if morning or evening:
                avail = DoctorAvailability(
                    doctor_id=doctor.id,
                    date=day_date,
                    morning_slot=morning,
                    evening_slot=evening
                )
                db.session.add(avail)

        db.session.commit()
        flash('Your availability has been updated successfully!', 'success')
        return redirect(url_for('doctor_dashboard'))

    return render_template('doctor_availability.html', next_7_days=next_7_days)

@app.route('/book_appointment/<int:doctor_id>/<date>/<slot>', methods=['POST'])
def book_appointment(doctor_id, date, slot):
    if session.get('user_type') != 'patient':
        flash('Access denied.', 'error')
        return redirect(url_for('home'))

    from datetime import datetime, time
    patient = Patient.query.get(session['user_id'])
    doctor = Doctor.query.get_or_404(doctor_id)

    appt_date = datetime.strptime(date, '%Y-%m-%d').date()

    if slot == 'morning':
        appt_time = time(10, 0, 0)
    elif slot == 'evening':
        appt_time = time(18, 0, 0)
    else:
        flash('Invalid slot.', 'error')
        return redirect(url_for('check_availability', doctor_id=doctor_id))

    appointment = Appointment(
        p_id=patient.id,
        d_id=doctor.id,
        date=appt_date,
        time=appt_time,
        status='Booked'
    )
    db.session.add(appointment)
    db.session.commit()

    flash(f'Appointment booked successfully with Dr. {doctor.name}!', 'success')
    return redirect(url_for('patient_dashboard'))

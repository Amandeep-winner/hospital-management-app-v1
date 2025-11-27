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
    return render_template('admin_dashboard.html')

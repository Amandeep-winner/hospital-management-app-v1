<div align="center">

<br/>

```text
██╗  ██╗ ██████╗ ███████╗██████╗ ██╗████████╗ █████╗ ██╗     
██║  ██║██╔═══██╗██╔════╝██╔══██╗██║╚══██╔══╝██╔══██╗██║     
███████║██║   ██║███████╗██████╔╝██║   ██║   ███████║██║     
██╔══██║██║   ██║╚════██║██╔═══╝ ██║   ██║   ██╔══██║██║     
██║  ██║╚██████╔╝███████║██║     ██║   ██║   ██║  ██║███████╗
╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝     ╚═╝   ╚═╝   ╚═╝  ╚═╝╚══════╝
```

<img src="https://cdn-icons-png.flaticon.com/512/2966/2966486.png" width="120" />

# 🏥 Hospital Management System

### **AI-Enhanced Healthcare Management Platform**

*Modernizing hospital workflows with intelligent automation, role-based systems, and scalable full-stack architecture.*

<br/>

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Web_Framework-black?style=for-the-badge\&logo=flask)
![SQLite](https://img.shields.io/badge/SQLite-Database-blue?style=for-the-badge\&logo=sqlite)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

<br/>

> 🚀 Designed to simulate real-world hospital workflows with scalable backend architecture, role-based dashboards, and future AI-powered healthcare assistance.

</div>

---

# 🚀 Why This Project Matters

Traditional hospital management systems are often fragmented, manual, and inefficient.

This platform aims to modernize healthcare operations through centralized workflow management, intelligent automation, and scalable full-stack architecture.

```text
Traditional Hospital Workflow              Hospital Management System
─────────────────────────────              ─────────────────────────────
❌ Manual patient tracking                 ✅ Centralized patient system
❌ Paper-based appointment flow            ✅ Digital appointment booking
❌ No workflow automation                  ✅ Role-based dashboards
❌ Disconnected departments                ✅ Unified management system
❌ Slow hospital operations                ✅ Streamlined administration
❌ Limited scalability                     ✅ AI-ready architecture
```

---

# 🌟 Core Features

## 🔐 Authentication & Role Management

* Secure login system for:

  * 👨‍💼 Admin
  * 👨‍⚕️ Doctor
  * 🧑 Patient
* Role-based access control

---

## 👨‍💼 Admin Dashboard

* Manage doctors
* Manage departments
* View registered patients
* Monitor hospital workflow

---

## 👨‍⚕️ Doctor Dashboard

* View assigned patients
* Update medical history
* Manage availability schedules

---

## 🧑‍🤝‍🧑 Patient Dashboard

* Patient registration & profile management
* Appointment booking
* View medical history
* Check doctor availability

---

# 🧠 AI Features (Planned Enhancements)

## 🤖 AI Symptom Checker

Analyze patient symptoms and suggest possible conditions with urgency estimation.

## 📄 AI Medical Report Summarizer

Summarize medical reports and highlight important insights automatically.

## 💬 AI Healthcare Assistant

Interactive chatbot for:

* Appointment support
* Doctor availability
* Patient guidance

---

# 🏗️ System Architecture

```text
                     ┌────────────────────────────┐
                     │   HOSPITAL MANAGEMENT APP  │
                     └────────────────────────────┘

        FRONTEND                 BACKEND                DATABASE
        ─────────                 ───────                ────────

     HTML / CSS UI  ───────►  Flask Application ─────► SQLite DB
                                    │
                                    │
                             SQLAlchemy ORM
                                    │
                                    ▼
                          Role-Based Controllers
                           (Admin / Doctor / Patient)

                                    │
                                    ▼
                          Future AI Integrations
                     (Symptom Checker • Chatbot • AI Reports)
```

---

# 🛠️ Tech Stack

| Layer            | Technology    |
| ---------------- | ------------- |
| **Backend**      | Flask, Python |
| **Database**     | SQLite        |
| **ORM**          | SQLAlchemy    |
| **Frontend**     | HTML, CSS     |
| **Architecture** | MVC Pattern   |

---

# 📸 Screenshots

> Add application screenshots here for better project presentation.

---

# 🎥 Demo Video

> Add a YouTube or Loom demo link here.

---

# ⚙️ Setup & Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/Amandeep-winner/hospital-management.git
cd hospital-management
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate

# Windows
venv\Scripts\activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Run Application

```bash
python app.py
```

🌐 App runs at:

```text
http://127.0.0.1:5000/
```

---

# 🔑 Default Credentials

| Role  | Username | Password |
| ----- | -------- | -------- |
| Admin | `admin`  | `admin`  |

---

# 📂 Project Structure

```bash
.
├── app.py
├── requirements.txt
├── application/
│   ├── controllers.py
│   ├── database.py
│   ├── models.py
│
├── templates/
├── static/
├── instance/
└── README.md
```

---

# 🔗 Project Origin & Attribution

This project was originally developed and maintained on an alternate GitHub account:

➡️ https://github.com/23f2003543/hospital-management-app-v1

The repository has now been migrated and enhanced with:

* Improved architecture
* Better documentation
* AI feature planning
* Modernized project presentation

---

# 🚀 Future Roadmap

```text
v1 (Current)                 v2 (Next Upgrade)             v3 (Future Vision)
────────────────────         ─────────────────────         ─────────────────────
✅ HMS core workflows         🔄 AI Symptom Checker         🔲 React Frontend
✅ Role-based dashboards      🔄 Medical AI Assistant       🔲 REST API Support
✅ Appointment system         🔄 Report Summarization       🔲 Cloud Deployment
✅ SQLite database            🔄 PostgreSQL Migration       🔲 SaaS Architecture
```

---

# 💼 What This Project Demonstrates

* Full-stack development using Flask
* Database design & ORM integration
* Role-based system architecture
* Healthcare workflow modeling
* Scalable backend design
* AI integration planning
* Real-world application structure

---

# 👨‍💻 Author

## Amandeep Singh

🚀 Focused on building scalable AI-powered applications, backend systems, and modern full-stack projects.

---

<div align="center">

### ⭐ If you found this project interesting, consider giving it a star on GitHub!

</div>

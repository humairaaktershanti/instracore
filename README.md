# InstraCore - Institute Management System



[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

[![Django Version](https://img.shields.io/badge/django-4.2+-green.svg)](https://www.djangoproject.com/)



InstraCore is a comprehensive role-based Institute Management System built with Django. It provides tailored dashboards and features for Admin, Employees (Faculty, HR, Finance, Marketing, IT, Teacher, and Others), and Students with strict permission control.



## 📋 Table of Contents



- [Features](#features)

- [Technology Stack](#technology-stack)

- [Installation](#installation)

- [Usage](#usage)

- [Project Structure](#project-structure)

- [User Roles & Permissions](#user-roles--permissions)

- [API Documentation](#api-documentation)

- [Contributing](#contributing)

- [License](#license)

- [Contact](#contact)



## ✨ Features



### Core Features

- **Role-based Access Control**: Different dashboards and permissions for Admin, Employees, and Students

- **User Management**: Admin can create and manage all user accounts; Students can self-register

- **Course Management**: Create, manage, and track online and offline courses

- **Attendance Tracking**: Monitor attendance for students, teachers, and staff

- **Financial Management**: Track fees, expenses, salaries, and transactions

- **Reporting System**: Generate and download reports for various data

- **Notification System**: Real-time notifications for important events

- **Event & Notice Management**: Create and manage events and notices



### Dashboard Features

- **Admin Dashboard**: Overview of students, teachers, courses, staff, attendance, accounts, and reports

- **Faculty Dashboard**: Course management, teacher assignments, and reviews

- **HR Dashboard**: Employee management, job postings, and interview scheduling

- **Finance Dashboard**: Salary management, expense tracking, and transaction approval

- **Teacher Dashboard**: Class routines, attendance, lesson plans, and course management

- **Student Dashboard**: Academic performance, fee tracking, resources, and certificates



## 🛠 Technology Stack



- **Backend**: Django 4.2+

- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript

- **Database**: SQLite (development), PostgreSQL (production recommended)

- **Authentication**: Django's built-in authentication system

- **Charts**: Chart.js for data visualization

- **Icons**: Bootstrap Icons



## 🚀 Installation



### Prerequisites

- Python 3.8 or higher

- pip package manager



### Setup



1. **Clone the repository**

&nbsp;  ```bash

&nbsp;  git clone https://github.com/thinkori/instracore.git

&nbsp;  cd instracore

&nbsp;  ```



2. **Create a virtual environment**

&nbsp;  ```bash

&nbsp;  python -m venv venv

&nbsp;  source venv/bin/activate  # On Windows: venvScriptsactivate

&nbsp;  ```



3. **Install dependencies**

&nbsp;  ```bash

&nbsp;  pip install -r requirements.txt

&nbsp;  ```



4. **Apply migrations**

&nbsp;  ```bash

&nbsp;  python manage.py makemigrations

&nbsp;  python manage.py migrate

&nbsp;  ```



5. **Create a superuser**

&nbsp;  ```bash

&nbsp;  python manage.py createsuperuser

&nbsp;  ```



6. **Collect static files**

&nbsp;  ```bash

&nbsp;  python manage.py collectstatic

&nbsp;  ```



7. **Run the development server**

&nbsp;  ```bash

&nbsp;  python manage.py runserver

&nbsp;  ```



8. **Access the application**

&nbsp;  Open your browser and navigate to `http://127.0.0.1:8000/`



## 📖 Usage



### Getting Started

1. Log in as the superuser to access the admin panel at `/admin/`

2. Create an Admin user through the admin panel

3. Create Employee accounts (Faculty, HR, Finance, etc.) through the admin panel

4. Students can self-register through the registration form



### Accessing Dashboards

- **Admin Dashboard**: `/admin/dashboard/`

- **Employee Dashboard**: `/employee/dashboard/` (redirects based on sub-role)

- **Student Dashboard**: `/student/dashboard/`



### Key Workflows

1. **Course Management**: Admin/Faculty can create courses and assign teachers

2. **Student Enrollment**: Students can browse and enroll in courses

3. **Attendance Tracking**: Teachers can mark attendance for their classes

4. **Fee Management**: Finance can track payments and generate reports

5. **HR Operations**: HR can post jobs, review applications, and schedule interviews



## 📁 Project Structure



```

instracore/
├── manage.py
├── requirements.txt
├── instracore/                 # Project configuration
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── AuthApp/                    # Authentication and user profiles
│   ├── models.py               # User, Notification, AuditLog, Trash models
│   ├── views.py                # Authentication views
│   ├── urls.py                 # Auth URLs
│   ├── forms.py                # User forms
│   └── templates/              # Auth templates
├── AdminApp/                   # Admin functionality
│   ├── models.py               # Event, Notice models
│   ├── views.py                # Admin dashboard and views
│   ├── urls.py                 # Admin URLs
│   └── templates/              # Admin templates
├── EmployeeApp/                # Employee functionality
│   ├── models.py               # JobPost, Application, Salary, Course, etc.
│   ├── views.py                # Employee dashboard and views
│   ├── urls.py                 # Employee URLs
│   └── templates/              # Employee templates
├── StudentApp/                 # Student functionality
│   ├── models.py               # Enrollment, ExamResult, Certificate, etc.
│   ├── views.py                # Student dashboard and views
│   ├── urls.py                 # Student URLs
│   └── templates/              # Student templates
├── static/                     # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── images/
├── media/                      # User-uploaded media
└── templates/                  # Base templates
&nbsp;   └── AuthApp/
&nbsp;       └── master.html          # Master template

```



## 👥 User Roles & Permissions



### Admin

- Full CRUD on all accounts (Admin, Employee, Student)

- Approve HR job posts

- View/download all reports

- Delete certificates

- Access to all system features



### Faculty

- Cannot create their own account (Admin only)

- CRUD on students

- Manage offline courses

- Review requests (course closure, teacher requirement)



### HR

- Create/manage job posts

- Offer salaries (Finance must approve)

- Schedule interviews

- Manage employees (excluding Admin)



### Finance

- Approve salaries & course pricing

- Track all financial data

- Generate monthly expense sheets

- Approve/reject transactions



### Teacher

- **Online**: Full course CRUD, sales tracking

- **Offline**: Accept/reject courses, manage students, assessments

- Create lesson plans and mark attendance

- Notify guardians



### Student

- Browse/register courses

- Access results, attendance, certificates

- Make payments and track fees

- Receive guardian notifications



## 🔌 API Documentation



The system doesn't currently have a dedicated REST API, but one can be implemented using Django REST Framework. Future enhancements may include:



- RESTful API endpoints for all major entities

- Authentication via JWT tokens

- Role-based API access control

- Documentation with Swagger/OpenAPI



## 🤝 Contributing



We welcome contributions to improve InstraCore! Please follow these steps:



1. **Fork the repository**

2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)

3. **Commit your changes** (`git commit -m 'Add amazing feature'`)

4. **Push to the branch** (`git push origin feature/amazing-feature`)

5. **Open a Pull Request**



### Development Guidelines

- Follow PEP 8 style guidelines

- Write meaningful commit messages

- Add tests for new features

- Update documentation as needed



## 📄 License



This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



## 📞 Contact



**Project Maintainer**

Khalid Mahmud

Email: khalid@thinkori.com

Website: https://thinkori.com



**Project Link**  

https://github.com/thinkori/instracore



---



**InstraCore** - Streamlining educational administration with technology.
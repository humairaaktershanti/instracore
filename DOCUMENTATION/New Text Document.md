# InstaCore — Institute Management System



> Full project documentation & step-by-step plan (Django)



---



## Table of Contents



1. Project Overview

2. Roles & Permissions (concept)

3. Key Features

4. Data Models (recommended)

5. User flows (index, signup, login, reset, delete)

6. Approval & Business Rules

7. Dashboard & UI mapping (templates + routes)

8. API design (REST endpoints and embed strategy)

9. Implementation: Step-by-step (development plan)

10. Dev environment & commands

11. Deployment checklist

12. Tests, fixtures & seeding

13. Security & operational notes

14. Appendix: sample endpoints, sample snippets, checklist for presentations



---



## 1. Project Overview



**InstaCore** is a Django-based Institute Management System that provides secure user onboarding, role-aware dashboards, profile management (including OTP-protected deletion), HR job-posting workflows, and future-ready REST APIs that other sites can embed/use.



Primary goals:



* Robust authentication (email verification + OTP flows)

* Role-based access and dashboards (student, teacher, HR, admin, finance, sales, marketing, IT...)

* Approval workflows for staff/hire/course changes

* Full audit trail for create/update/delete actions (timestamped)

* Provide CRUD and API endpoints that can be embedded into third-party sites



---



## 2. Roles & Permissions (concept)



**Roles (example):**



* `ADMIN` (full system power)

* `HR` (job posts, manage employees)

* `ACCOUNT` / `FINANCE` (transactions, payments)

* `TEACHER` (create/manage courses, accept students)

* `STUDENT` (apply/enroll in courses)

* `SALES` / `MARKETING` (manage course publication / pricing)

* `IT` (technical operations)

* `GUEST` (public viewers)



**Permission rules (high level):**



* `ADMIN` can perform all CRUD operations on users, courses, job posts, and finance records.

* `HR` can post jobs, review applications; `ADMIN` or `FINANCE` must approve hires for employee accounts that affect payroll.

* `TEACHER` can create courses (requires `ADMIN` + `SALES` approval to publish/remove)

* `STUDENT` can signup and request enrollments; enrollment approval may be required by the assigned `TEACHER` or `ADMIN` depending on the course.



Implementation tip: use Django's `PermissionsMixin` and custom decorators( or DRF `IsAuthenticated` + custom permission classes) to enforce role checks.



---



## 3. Key Features (phase-aware)



**Phase 1 (must-have for first demo):**



* Landing page (`index.html`) with two clear CTA buttons: `Login` and `Signup`

* Signup with email verification

* Login with "Forgot Password" (email OTP reset)

* Custom `User` with `role` field (enum) — user profiles editable, deletable (delete must be confirmed by OTP)

* Individual dashboards after login (role-aware)

* Navigation bar that updates based on login/role and a fixed footer



**Phase 2 (next follow-up / API demo):**



* CRUD for Courses, Departments, and Enrollments

* HR: Job posts + applications management

* Finance: Simple transactions/records and linking to course registrations

* REST API endpoints (Auth + CRUD) and an embeddable widget



**Phase 3 (final):**



* Role-based advanced modules: attendance, results, announcements

* API docs (Swagger/Redoc), JWT tokens for external apps

* Production hardening: PostgreSQL, Celery for background emails/OTP expiry, CDN for static files



---



## 4. Data Models (recommended)



Below are suggested Django models and important fields. Use `created_at`, `updated_at` and track `status` where appropriate.



### `users.models.CustomUser`



* `id` (UUID or AutoField)

* `email` (unique)

* `full_name`

* `role` (choices: ADMIN, HR, TEACHER, STUDENT, ACCOUNT, FINANCE, SALES, MARKETING, IT, GUEST)

* `is_active`, `is_staff`

* `email_verified` (bool)

* `date_joined`

* `profile_image` (optional)

* `phone`, `address` (optional)

* `department` (FK -> `Department`, nullable)



**Use:** `AUTH_USER_MODEL = 'users.CustomUser'`



---



### `users.models.Profile` (optional)



* `user` (OneToOne -> CustomUser)

* `bio`, `dob`, `gender`, extra contact fields



Use if you want to keep `CustomUser` minimal.



---



### `core.models.Department`



* `name`, `code`, `description`

* `head` (FK -> CustomUser)



---



### `courses.models.Course`



* `title`, `code`, `description`

* `teacher` (FK -> CustomUser, role TEACHER)

* `fee`, `max_seats`, `status` (DRAFT/PENDING/ACTIVE/ARCHIVED)

* `created_at`, `updated_at`



---



### `courses.models.Enrollment`



* `student` (FK -> CustomUser with role STUDENT)

* `course` (FK -> Course)

* `status` (APPLIED/ENROLLED/REJECTED/CANCELLED)

* `applied_at`, `enrolled_at`



Business rule: enrolling may require teacher/admin approval.



---



### `hr.models.JobPost`



* `title`, `description`, `department` (FK)

* `created_by` (FK -> CustomUser with HR/Admin)

* `status` (OPEN/CLOSED/FILLED)

* `created_at`, `expires_at`



---



### `hr.models.JobApplication`



* `applicant` (FK -> CustomUser or external email record)

* `job_post` (FK)

* `resume` (FileField)

* `status` (APPLIED/SHORTLISTED/REJECTED/HIRED)

* `applied_at`



---



### `finance.models.Transaction` (simple)



* `user` (FK -> CustomUser)

* `amount`, `transaction_type` (PAYMENT/REFUND/SALARY/OTHER)

* `reference_id`, `status` (PENDING/COMPLETED/FAILED)

* `created_at`



---



### `auth.models.OTP` (one table for all purposes)



* `user` (FK -> CustomUser)

* `code` (6-digit)

* `purpose` (EMAIL_VERIFY / PASSWORD_RESET / ACCOUNT_DELETE)

* `is_used` (bool)

* `created_at`, `expires_at`

* `attempts` (int)



Business rule: OTP expires (e.g., 10 minutes), limit attempts to 3, store IP if needed.



---



### `core.models.AuditLog`



* `actor` (FK -> CustomUser, nullable for system tasks)

* `action` (CREATE/UPDATE/DELETE/APPROVE/REJECT)

* `model_name`, `object_id`

* `changes` (JSONField)

* `timestamp`

* `ip_address` (optional)



Use AuditLog to record every create/update/delete along with who did it and when.



---



## 5. User flows (index, signup, login, reset, delete)



**Index (`index.html`)**



* Two big CTA buttons: `Login` and `Signup`

* Public info about the institute and a footer



**Signup flow**



1. User clicks `Signup` → fills form (name, email, password, role selection)

2. Save user as `is_active=False`, `email_verified=False` and create `OTP` with purpose `EMAIL_VERIFY` (or token)

3. Send verification email with secure token/OTP link

4. User clicks link or enters OTP → verify → set `email_verified=True`, `is_active=True` (if no admin approval required)

5. If role requires admin approval (staff roles), set status to `PENDING_APPROVAL` and inform admin/HR



**Login flow**



* Standard Django login using email + password (or username if used)

* If `email_verified` is False, block or show a message to verify

* After login, redirect to `/dashboard/` (role-based)



**Forgot password**



1. Click `Forgot` → input registered email

2. Generate OTP with `PASSWORD_RESET` purpose and send to email

3. User enters OTP → allowed to set a new password

4. Clear OTP or mark `is_used`



**Delete account**



* In profile settings, `Delete Account` triggers OTP (ACCOUNT_DELETE) sent to email

* On OTP verify, either mark `is_active=False` (soft delete) or delete the record while keeping `AuditLog`



Soft-delete recommendation: set `is_active=False` and keep user data for auditing and integrity of foreign keys. Provide explicit admin delete for hard delete.



---



## 6. Approval & Business Rules



**Signup & account activation**



* Students: can auto-activate after email verification OR require admin registration acceptance based on institute policy.

* Teachers/HR/Account/Finance: signup should create a `PENDING` account that requires `ADMIN` approval (and optionally `HR` approval for payroll setup).

* If an HR or Accounts role doesn’t exist (not signed up yet), allow `ADMIN` to assume/override to accept new employees.



**Course creation & deletion**



* Teacher can create a course as `DRAFT` or `PENDING`.

* For a course to be `ACTIVE` and visible to students, it must be approved by `ADMIN` and `SALES`/`FINANCE` (since it has pricing and revenue implications).

* Deleting a course requires approval from `ADMIN` + `SALES` if it impacts finances — record these approvals in `AuditLog`.



**Enrollments**



* Student can apply/enroll. The `TEACHER` may approve or reject. Admin may override.



**Job posts & hiring**



* HR posts job; applicants apply via signup or as guests (capture email + CV). HR/Accounts and Admin approve hiring. If HR not present, Admin temporarily acts.



---



## 7. Dashboard & UI mapping (templates + routes)



**Template naming convention** (under `templates/`):



* `base.html` — main layout with nav, static footer, and blocks

* `index.html` — landing

* `auth/signup.html`, `auth/login.html`, `auth/email_verify.html`, `auth/password_reset.html`

* `dashboard/base_dashboard.html` (shared layout for dashboards)

* `dashboard/admin/index.html`, `dashboard/teacher/index.html`, `dashboard/student/index.html`, `dashboard/hr/index.html`

* `profile/view.html`, `profile/edit.html`, `profile/delete_confirm.html`

* `courses/list.html`, `courses/detail.html`, `courses/manage.html`

* `hr/job_list.html`, `hr/post_detail.html`, `hr/applications.html`



**URL mapping (suggested)**



```

/                  -> index

/accounts/signup/  -> signup

/accounts/verify/  -> verify email (token/OTP)

/accounts/login/   -> login

/accounts/forgot/  -> request password OTP

/accounts/reset/   -> password reset (OTP)

/dashboard/        -> redirect to role dashboard

/dashboard/admin/  -> admin dashboard

/dashboard/teacher/-> teacher dashboard

/profile/          -> profile view

/profile/edit/     -> profile edit

/profile/delete/   -> delete account (OTP flow)

/courses/          -> courses listing

/courses/<id>/     -> course detail

/hr/jobs/          -> job posts

/hr/apply/<job>/   -> apply

/api/...           -> API endpoints (see next section)

```



**Navigation & footer**



* Top nav: `Logo | Home | Courses | Jobs | (Role-aware links) | Profile Icon` (profile icon shows drop-down)

* Fixed footer: Institute name, contact, quick links, copyright



---



## 8. API design (REST endpoints and embed strategy)



**Auth endpoints (public)**



* `POST /api/auth/register/` — register user (returns pending status)

* `POST /api/auth/verify-email/` — verify OTP/token

* `POST /api/auth/login/` — returns JWT or token

* `POST /api/auth/password-reset/` — request OTP

* `POST /api/auth/password-reset-confirm/` — confirm OTP & set password

* `POST /api/auth/logout/` — invalidate token



**User & Profile endpoints**



* `GET /api/users/` — list (admin only)

* `GET /api/users/<id>/` — retrieve

* `PATCH /api/users/<id>/` — update (role-based)

* `DELETE /api/users/<id>/` — delete (admin or owner)



**Course & Enrollment endpoints**



* `GET /api/courses/` — public listing (published only)

* `POST /api/courses/` — create (teacher, but needs approval)

* `GET /api/courses/<id>/` — detail

* `POST /api/courses/<id>/enroll/` — student apply/enroll

* `PATCH /api/enrollments/<id>/approve/` — teacher/admin approve



**HR endpoints**



* `GET /api/jobs/`, `POST /api/jobs/` (HR/Admin)

* `POST /api/jobs/<id>/apply/` — upload resume

* `PATCH /api/applications/<id>/` — update status (HR/Admin)



**Finance endpoints**



* `GET /api/transactions/` — finance/admin

* `POST /api/transactions/record/` — record payment



**Embedding strategy (simple)**

Provide a small embeddable JS snippet other sites can place on a page to use InstaCore auth/mini-forms. Example flow:



1. Create a public endpoint that serves a widget JS (e.g. `https://instacore.example/embed/widget.js`).

2. The widget renders a small iframe or modal that points to `https://instacore.example/embed/auth-widget?client_id=XYZ`.

3. Widget performs OAuth-like or token-based handshake:



&nbsp;  * Owner registers for a `client_id` and `client_secret` in your system.

&nbsp;  * When the embedded widget needs to call protected endpoints, it uses a short-lived token requested from your API using the `client_id` + a server-side callback.



**Simpler alternative for demo:** embed unauthenticated `signup` or `apply job` forms that POST to your public API (`/api/embed/signup/`) which sends verification email and returns embed success. Secure by enabling origin checks and rate limits.



---



## 9. Implementation: Step-by-step (development plan)



This section is a linear task list you (the team) can follow. Assume a Git repo `instacore-institute-management` and each major feature as a branch.



### Preparation (Day 0)



1. Create repo & README (branch `main`).

2. Create GitHub project or board for tasks (To Do / In Progress / Done).

3. Assign roles in the team and split tasks.



### Step 1 — Project scaffolding (Day 1)



1. Create virtualenv & install packages.



&nbsp;  ```bash

&nbsp;  python -m venv .venv

&nbsp;  source .venv/bin/activate

&nbsp;  pip install django djangorestframework djangorestframework-simplejwt psycopg2-binary pillow django-cors-headers django-crispy-forms

&nbsp;  ```

2. Start project and apps:



&nbsp;  ```bash

&nbsp;  django-admin startproject instacore

&nbsp;  cd instacore

&nbsp;  python manage.py startapp users

&nbsp;  python manage.py startapp courses

&nbsp;  python manage.py startapp hr

&nbsp;  python manage.py startapp finance

&nbsp;  python manage.py startapp core

&nbsp;  python manage.py startapp api  # optional: unify DRF views

&nbsp;  ```

3. Add apps to `INSTALLED_APPS` and set `AUTH_USER_MODEL = 'users.CustomUser'` in `settings.py`.



### Step 2 — Custom user & auth (Day 2-3)



1. Implement `CustomUser` model with role choices.

2. Create `Profile` model (optional) and `OTP` model.

3. Create and run migrations:



&nbsp;  ```bash

&nbsp;  python manage.py makemigrations

&nbsp;  python manage.py migrate

&nbsp;  ```

4. Create superuser:



&nbsp;  ```bash

&nbsp;  python manage.py createsuperuser

&nbsp;  ```

5. Implement signup view/form and email verification flow using Django email backend.



&nbsp;  * For development: use `EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'`.

&nbsp;  * Later configure SMTP vars in environment.



### Step 3 — Login, password reset, OTP flows (Day 4)



1. Build login view and `Forgot Password` → `OTP` sending and confirm flow.

2. Implement `Account Delete` flow with OTP validation — on confirm, soft-delete the user (`is_active=False`) and log action in `AuditLog`.



### Step 4 — Dashboards & role-based templates (Day 5-7)



1. Build `base.html` with nav + footer. Add responsive CSS/Bootstrap.

2. Create dashboard base and specific dashboard pages for roles.

3. Add menu items that change based on `request.user.role`.



### Step 5 — Core features: Courses, Enrollments, HR (Day 8-12)



1. Implement `Course`, `Enrollment` models and templates.

2. Implement course creation by `TEACHER` and approval flow for publishing.

3. Implement `JobPost` and `JobApplication` with resume upload.

4. Add `Finance` models and simple transactions.



### Step 6 — Admin & approval pages (Day 13-15)



1. Add admin panel custom pages where `ADMIN` can approve pending staff, courses, and transactions.

2. Add notifications/emails that notify relevant parties on pending approvals.



### Step 7 — API (Day 16-19)



1. Add DRF serializers & viewsets for Auth, Users, Courses, Enrollments, Jobs, and Transactions.

2. Add JWT auth (SimpleJWT) or TokenAuth for API consumers.

3. Implement basic rate-limiting and CORS.



### Step 8 — Embed widget & docs (Day 20-22)



1. Create an embeddable widget (JS) that can render signup/login forms or link to an overlay iframe.

2. Document `client_id` workflow for embed partners.



### Step 9 — Testing, polishing & final touches (Day 23-24)



1. Write unit tests for critical auth flows: signup, verify, OTP, password reset.

2. Create sample data fixtures for demo users (admin, teacher, student, HR).

3. Polish CSS and responsiveness. Optimize assets.



### Step 10 — Final deployment (Day 25)



1. Prepare production settings, collect static files, setup environment variables.

2. Deploy to chosen host (instructions in next section).



> Note: These day estimates assume the team works together and can overlap tasks. Adjust as needed.



---



## 10. Dev environment & commands



**Recommended packages**



* `django`, `djangorestframework`, `djangorestframework-simplejwt`, `psycopg2-binary`, `Pillow`, `django-cors-headers`, `django-crispy-forms`



**Common commands:**



```bash

# Start dev server

python manage.py runserver



# Make migrations

python manage.py makemigrations

python manage.py migrate



# Create superuser

python manage.py createsuperuser



# Run tests

python manage.py test



# Create fixture

python manage.py loaddata initial_data.json



# Collect static for production

python manage.py collectstatic

```



**Sample `settings.py` snippets**



```py

INSTALLED_APPS += [

&nbsp;   'rest_framework', 'corsheaders', 'crispy_forms',

&nbsp;   'users','courses','hr','finance','core','api'

]



AUTH_USER_MODEL = 'users.CustomUser'



# Dev email

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'



# Simple JWT example

REST_FRAMEWORK = {

&nbsp;   'DEFAULT_AUTHENTICATION_CLASSES': (

&nbsp;       'rest_framework_simplejwt.authentication.JWTAuthentication',

&nbsp;   ),

}

```



---



## 11. Deployment checklist (minimal)



* Use PostgreSQL in production

* Configure environment variables (SECRET_KEY, DB, EMAIL_HOST_USER/PASS)

* Use Gunicorn + Nginx (or host on Railway / Render / Dokku / PythonAnywhere)

* Setup HTTPS (Let's Encrypt)

* Run `collectstatic`

* Setup logs and monitoring

* Setup periodic backup of DB



---



## 12. Tests, fixtures & seeding



* Create fixtures for: roles, admin user, demo teacher, demo student, sample courses

* Write tests for:



&nbsp; * Signup + email verification flow

&nbsp; * OTP expiration and limit checks

&nbsp; * Login + protected route access

&nbsp; * Course create/approval flow



Sample fixture names: `fixtures/initial_roles.json`, `fixtures/demo_users.json`, `fixtures/sample_courses.json`.



---



## 13. Security & operational notes



* **Passwords:** rely on Django's hashing — never log passwords

* **OTP:** limit attempts, expire quickly (10 min recommended), and throttle requests to prevent abuse

* **Email tokens:** use Django `signing` or JWT for email verification links

* **Audit logs:** store detailed JSON of changes for sensitive operations (delete, role-change, course publish)

* **Soft-delete:** prefer `is_active=False` to avoid orphaned FK constraints

* **Backups:** daily DB snapshot for production

* **Rate-limits:** for public endpoints (signup, login) to prevent abuse



---



## 14. Appendix



### Sample API endpoints quick list



```

POST /api/auth/register/

POST /api/auth/verify-email/ (otp/token)

POST /api/auth/login/

POST /api/auth/password-reset/

POST /api/auth/password-reset-confirm/

GET  /api/courses/

POST /api/courses/ (teacher -> pending)

POST /api/courses/<id>/enroll/

GET  /api/jobs/

POST /api/jobs/<id>/apply/

```



### Sample small JS embedding idea (demo only)



```html

<!-- partner page includes this -->

<script src="https://instacore.example/embed/widget.js" data-client="CLIENT_ID"></script>

```



The widget opens an iframe `https://instacore.example/embed/auth-widget?client=CLIENT_ID` that serves a minimal signup/login UI.



### Presentation checklist for Day 1



* [ ] Mockups ready (Humaira)

* [ ] Leader script (Khalid)

* [ ] Timeline & planning slides (Mehedi)

* [ ] Mockup walkthrough (Shakil)

* [ ] Create demo accounts and sample screenshots



---



## Final notes



This document is intentionally implementation-focused and iterative. Start with Phase 1 features and keep Phase 2/3 as planned expansions. Keep commits small and use branches for features. Add documentation to the repo `README.md` with this content or a summarized version for public view.



Good luck — ping me if you want this exported as a `.md` file in the repo or if you want me to generate example model files and serializer stubs next.




# 📚 InstaCore – Institute Management System



*A Django-based platform for modern institute operations with authentication, email/OTP verification, profile management, role-based dashboards, and administrative workflows.*



---



## **1. Project Overview**



InstaCore is a **secure and role-based Institute Management System** designed to handle both academic and administrative workflows in a single platform.

It offers **role-specific dashboards**, **profile management**, **email & OTP verification**, and **approval workflows** for important institute activities.



---



## **2. Roles & Permissions**



| Role                        | Permissions                                                                                                                  |

| --------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |

| **Admin**                   | Full control over system. Manage all members, approve signups, assign roles, add/delete courses, remove any member.          |

| **HR**                      | Approve employee accounts, create/manage job posts, hire new staff (with admin/account approval).                            |

| **Teacher**                 | Manage own courses, add/remove students (from their own courses only), create new courses (requires admin & sales approval). |

| **Student**                 | Access own dashboard, enroll in courses (requires teacher approval), manage own profile.                                     |

| **Sales**                   | Approve course additions/removals (due to financial implications).                                                           |

| **Accounts**                | Approve employee hiring, manage finance-related permissions.                                                                 |

| **Marketing / IT / Others** | Dashboard with limited tools relevant to their department.                                                                   |



---



## **3. Pages & Workflows**



### **3.1 Index Page (`index.html`)**



* **Elements:**



&nbsp; * Welcome message

&nbsp; * **Login** button → `/login`

&nbsp; * **Signup** button → `/signup`

* **Features:**



&nbsp; * Modern UI with static header/footer

&nbsp; * Responsive navigation bar

&nbsp; * Navigation changes based on authentication status



---



### **3.2 Signup Page (`signup.html`)**



* **Workflow:**



&nbsp; 1. User fills signup form.

&nbsp; 2. Email verification sent.

&nbsp; 3. User confirms email → account status: **Pending Approval**.

&nbsp; 4. Approval workflow:



&nbsp;    * Student → Teacher approval required.

&nbsp;    * Employee (Teacher, HR, Sales, etc.) → HR + Accounts + Admin approval.

&nbsp;    * HR / Accounts missing? → Admin handles their part.

* **Tech:**



&nbsp; * Django Custom User Model with `role` field.

&nbsp; * Email verification via Django's email backend.



---



### **3.3 Login Page (`login.html`)**



* **Workflow:**



&nbsp; 1. Enter email & password.

&nbsp; 2. Forgot password option → Email OTP for reset.

* **Post-login Redirect:**



&nbsp; * Based on `role` → Specific dashboard.



---



### **3.4 Dashboard Pages**



**Dynamic dashboard layout per role**:



* **Admin Dashboard**:



&nbsp; * View/manage all members

&nbsp; * Approve/reject signups

&nbsp; * Manage courses (create/update/delete with sales approval)

&nbsp; * Manage own profile

* **HR Dashboard**:



&nbsp; * Job posting

&nbsp; * Employee approval process

&nbsp; * Profile management

* **Teacher Dashboard**:



&nbsp; * Manage courses they own

&nbsp; * Approve student enrollments

&nbsp; * Remove students from their courses

* **Student Dashboard**:



&nbsp; * Enroll in courses (with teacher approval)

&nbsp; * View enrolled courses

&nbsp; * Manage profile

* **Sales Dashboard**:



&nbsp; * Approve/deny course creation/deletion

* **Accounts Dashboard**:



&nbsp; * Employee approvals

&nbsp; * Financial permissions



---



### **3.5 Profile Management**



* View profile

* Edit profile

* Change password

* Delete account (requires email OTP confirmation)

* Logout



---



## **4. Account Deletion Rules**



* **User-Initiated**:



&nbsp; * Requires OTP sent to email.

* **Admin-Initiated**:



&nbsp; * Admin can delete any account.

* **Teacher-Initiated**:



&nbsp; * Can remove students from their own courses only.



---



## **5. Course Management**



* **Create Course**:



&nbsp; * Teacher initiates → Requires admin + sales approval.

* **Delete Course**:



&nbsp; * Requires admin + sales approval.

* **Enroll Student**:



&nbsp; * Student requests → Teacher approval.

* **Remove Student**:



&nbsp; * Teacher can remove from their course.



---



## **6. Job Posting & Hiring Workflow**



* HR can post jobs.

* Applicants must sign up.

* Approval required from **Admin + Accounts + HR**.

* If HR or Accounts role not yet created → Admin acts on their behalf.



---



## **7. Approval & Logging**



* All create/update/delete actions:



&nbsp; * Require saving into **Approval Models** with timestamp.

&nbsp; * Admins and relevant roles can see pending actions.

&nbsp; * Logs stored for audit.



---



## **8. Technical Implementation**



* **Backend:** Django (Custom User Model, Role-Based Permissions)

* **Frontend:** HTML, CSS (Bootstrap), JavaScript

* **Database:** SQLite (dev) / PostgreSQL (production)

* **Auth:** Django Custom Authentication + Email Verification + OTP

* **API:** Planned REST API with Django REST Framework

* **Security:** OTP for sensitive actions, role-based views, CSRF protection



---



## **9. Future Features**



* Notifications & announcements

* Attendance tracking

* Grades & results

* API embedding for external integration

* Multi-language support


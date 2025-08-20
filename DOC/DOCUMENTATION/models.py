# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid

# -------------------------
# 1. Custom User & Roles
# -------------------------
class User(AbstractUser):
    USER_ROLES = [
        ('admin', 'Admin'),
        ('hr', 'HR'),
        ('accounts', 'Accounts'),
        ('sales', 'Sales'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('marketing', 'Marketing'),
        ('it', 'IT'),
        ('other', 'Other')  #The "other" role in your USER_ROLES list is basically a catch-all category — (e.g., librarian, security guard, maintenance worker, guest lecturer, etc.)
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=USER_ROLES)
    status = models.CharField(max_length=20, default='pending')  # pending, active, suspended
    email_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'role']

    def __str__(self):
        return f"{self.username} ({self.role})"


# -------------------------
# 2. Profile (One-to-One)
# -------------------------
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    contact_info = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=32, blank=True, null=True)
    photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"


# -------------------------
# 3. Parent - Student relation
# -------------------------
class Parent(models.Model):
    """
    Represents a parent/guardian record.
    If the parent also has an account on the system, link to User via parent_user.
    A Parent can be linked to many students (ManyToMany).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent_user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True,
                                       help_text="If parent has an account, link here.")
    full_name = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=32, blank=True, null=True)
    relation = models.CharField(max_length=64, blank=True, null=True)  # e.g., Father, Mother, Guardian
    created_at = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField('User', related_name='parents', limit_choices_to={'role': 'student'})

    def __str__(self):
        return f"{self.full_name} ({self.phone or 'no-phone'})"


# -------------------------
# 4. Course & Seat Assignment
# -------------------------
class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=32, blank=True, null=True)
    description = models.TextField(blank=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    created_at = models.DateTimeField(auto_now_add=True)

    # seat management
    total_seats = models.PositiveIntegerField(default=0)
    seats_filled = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def has_available_seat(self):
        return self.seats_filled < self.total_seats


class SeatAssignment(models.Model):
    """
    Tracks seat assignment (for classrooms, seat numbers etc.)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='seat_assignments')
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    seat_number = models.CharField(max_length=20, blank=True, null=True)
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('course', 'seat_number')  # prevent duplicate seat numbers per course

    def __str__(self):
        return f"{self.student.username} -> {self.course.name} (Seat {self.seat_number})"


# -------------------------
# 5. Enrollment
# -------------------------
class Enrollment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)
    enrolled_at = models.DateTimeField(null=True, blank=True)

    def approve(self, approver):
        """Call to approve an enrollment (set timestamps, increment seat counters, log approval)."""
        if self.status != 'active':
            # seat check
            if not self.course.has_available_seat():
                raise ValueError("No seats available")
            self.status = 'active'
            self.enrolled_at = timezone.now()
            self.course.seats_filled = models.F('seats_filled') + 1
            self.course.save(update_fields=['seats_filled'])
            self.save(update_fields=['status', 'enrolled_at'])

    def __str__(self):
        return f"{self.student.username} -> {self.course.name} ({self.status})"


# -------------------------
# 6. Job Posting (salary)
# -------------------------
class JobPost(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('pending', 'Pending')
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    department = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True)
    hr = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'hr'})
    salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True,
                                 help_text="Monthly salary or proposed compensation")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    posted_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.status})"


class JobApplication(models.Model):
    STATUS = [
        ('applied', 'Applied'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
        ('hired', 'Hired')
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                  help_text="If applicant has an account")
    applicant_name = models.CharField(max_length=200)
    applicant_email = models.EmailField()
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='applied')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.applicant_name} -> {self.job.title}"


# -------------------------
# 7. Approval System (reused)
# -------------------------
class Approval(models.Model):
    ACTION_CHOICES = [
        ('add_course', 'Add Course'),
        ('delete_course', 'Delete Course'),
        ('add_user', 'Add User'),
        ('delete_user', 'Delete User'),
        ('enroll_student', 'Enroll Student'),
        ('add_job', 'Add Job'),
        ('delete_job', 'Delete Job'),
        ('leave_request', 'Leave Request'),
        ('salary_approval', 'Salary Approval'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    action_type = models.CharField(max_length=50, choices=ACTION_CHOICES)
    target_id = models.UUIDField(null=True, blank=True)
    requested_by = models.ForeignKey(User, related_name='requests', on_delete=models.CASCADE)
    approved_by = models.ForeignKey(User, related_name='approvals', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, default='pending')
    timestamp = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.action_type} ({self.status})"


# -------------------------
# 8. Leave Management
# -------------------------
class LeaveRequest(models.Model):
    LEAVE_STATUS = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leave_requests')
    # if a student, optionally record parent approval/notification
    parent = models.ForeignKey(Parent, on_delete=models.SET_NULL, null=True, blank=True,
                               help_text="Parent who approved/requested (if applicable)")
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=LEAVE_STATUS, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)
    actioned_at = models.DateTimeField(null=True, blank=True)
    actioned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='leave_actions')

    def __str__(self):
        return f"Leave[{self.user.username}] {self.start_date} -> {self.end_date} ({self.status})"


# -------------------------
# 9. Results (grades)
# -------------------------
class Result(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    marks_obtained = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    total_marks = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    grade = models.CharField(max_length=8, blank=True, null=True)
    published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    published_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='published_results')

    def __str__(self):
        return f"Result: {self.student.username} - {self.course.name}"


# -------------------------
# 10. Finance / Student Account
# -------------------------
class StudentAccount(models.Model):
    """
    Track pending money, payments, refunds for a student.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'}, related_name='account')
    pending_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.username} Account - Pending: {self.pending_balance}"


class FinanceTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
        ('payment', 'Payment'),
        ('refund', 'Refund'),
        ('salary', 'Salary')
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True)
    student = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                help_text="If this transaction relates to a student")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='transactions_created')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"


# -------------------------
# 11. Notifications (Email / SMS)
# -------------------------
class Notification(models.Model):
    NOTIF_TYPES = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('push', 'Push')
    ]
    STATUS = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed')
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    to_parent = models.ForeignKey(Parent, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    notif_type = models.CharField(max_length=10, choices=NOTIF_TYPES)
    subject = models.CharField(max_length=255, blank=True)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    meta = models.JSONField(blank=True, null=True)  # e.g., {'sms_provider_id': 'xxx', 'provider_status': '...'}
    related_object = models.CharField(max_length=100, blank=True, null=True)  # e.g., 'leave:UUID' or 'result:UUID'

    def __str__(self):
        target = self.to_user or self.to_parent
        return f"Notification to {target} ({self.notif_type}) - {self.status}"


# -------------------------
# 12. Edit / Audit History
# -------------------------
class EditHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    model_name = models.CharField(max_length=50)
    object_id = models.UUIDField()
    action = models.CharField(max_length=20)  # created, updated, deleted
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    changes = models.JSONField(blank=True, null=True)  # store changes as JSON

    def __str__(self):
        return f"{self.action} on {self.model_name} by {self.performed_by}"

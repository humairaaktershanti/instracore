from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid


# =========================
# 1. Custom User & Roles
# =========================
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
        ('other', 'Other')
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


# =========================
# 2. Profile (One-to-One)
# =========================
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    contact_info = models.CharField(max_length=255, blank=True)
    photo = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"


# =========================
# 3. Course & Enrollment
# =========================
class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Enrollment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected')
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} -> {self.course.name}"


# =========================
# 4. Job Posting
# =========================
class JobPost(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('pending', 'Pending')
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    description = models.TextField()
    hr = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'hr'})
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# =========================
# 5. Approval System
# =========================
class Approval(models.Model):
    ACTION_CHOICES = [
        ('add_course', 'Add Course'),
        ('delete_course', 'Delete Course'),
        ('add_user', 'Add User'),
        ('delete_user', 'Delete User'),
        ('enroll_student', 'Enroll Student'),
        ('add_job', 'Add Job'),
        ('delete_job', 'Delete Job')
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    action_type = models.CharField(max_length=50, choices=ACTION_CHOICES)
    target_id = models.UUIDField()
    requested_by = models.ForeignKey(User, related_name='requests', on_delete=models.CASCADE)
    approved_by = models.ForeignKey(User, related_name='approvals', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, default='pending')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action_type} ({self.status})"


# =========================
# 6. Finance / Cash Tracking
# =========================
class FinanceTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense')
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"


# =========================
# 7. History Logs
# =========================
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

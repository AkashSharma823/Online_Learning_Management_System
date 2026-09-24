from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    ROLE_CHOICES = [("student","Student"),("instructor","Instructor"),("admin","Admin")]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="student")
    avatar = models.URLField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"{self.user.username} ({self.role})"

class Category(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    def __str__(self): return self.name

class Course(models.Model):
    LEVELS = [("Beginner","Beginner"),("Intermediate","Intermediate"),("Advanced","Advanced")]
    instructor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="courses")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="courses")
    title = models.CharField(max_length=220)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    thumbnail = models.URLField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    level = models.CharField(max_length=30, choices=LEVELS, default="Beginner")
    duration = models.CharField(max_length=80, default="8 weeks")
    published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=220)
    description = models.TextField(blank=True)
    video_url = models.URLField(blank=True)
    duration_minutes = models.PositiveIntegerField(default=15)
    order = models.PositiveIntegerField(default=1)
    free_preview = models.BooleanField(default=False)

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    progress = models.PositiveIntegerField(default=0)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    class Meta:
        constraints = [models.UniqueConstraint(fields=["student","course"], name="unique_enrollment")]

class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="assignments")
    title = models.CharField(max_length=220)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    points = models.PositiveIntegerField(default=100)

class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="quizzes")
    title = models.CharField(max_length=220)
    questions = models.PositiveIntegerField(default=10)
    duration_minutes = models.PositiveIntegerField(default=20)

class Exam(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="exams")
    title = models.CharField(max_length=220)
    exam_date = models.DateField(null=True, blank=True)
    duration_minutes = models.PositiveIntegerField(default=60)
    total_marks = models.PositiveIntegerField(default=100)

class Certificate(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="certificates")
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    certificate_no = models.CharField(max_length=80, unique=True)
    issued_at = models.DateField(auto_now_add=True)

class Review(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveIntegerField(default=5)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField(max_length=220)
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    subject = models.CharField(max_length=220)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Attendance(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    present = models.BooleanField(default=True)

class LiveClass(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="live_classes")
    title = models.CharField(max_length=220)
    starts_at = models.DateTimeField()
    meeting_url = models.URLField(blank=True)

class SupportTicket(models.Model):
    STATUS = [("Open","Open"),("Pending","Pending"),("Resolved","Resolved")]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=220)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS, default="Open")
    created_at = models.DateTimeField(auto_now_add=True)

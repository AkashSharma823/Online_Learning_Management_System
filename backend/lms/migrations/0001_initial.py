from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("description", models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name="Profile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("role", models.CharField(choices=[("student", "Student"), ("instructor", "Instructor"), ("admin", "Admin")], default="student", max_length=20)),
                ("avatar", models.URLField(blank=True)),
                ("phone", models.CharField(blank=True, max_length=30)),
                ("bio", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="profile", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="Course",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=220)),
                ("slug", models.SlugField(unique=True)),
                ("description", models.TextField(blank=True)),
                ("thumbnail", models.URLField(blank=True)),
                ("price", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ("level", models.CharField(choices=[("Beginner", "Beginner"), ("Intermediate", "Intermediate"), ("Advanced", "Advanced")], default="Beginner", max_length=30)),
                ("duration", models.CharField(default="8 weeks", max_length=80)),
                ("published", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("category", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="courses", to="lms.category")),
                ("instructor", models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="courses", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="Assignment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=220)),
                ("description", models.TextField(blank=True)),
                ("due_date", models.DateField(blank=True, null=True)),
                ("points", models.PositiveIntegerField(default=100)),
                ("course", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="assignments", to="lms.course")),
            ],
        ),
        migrations.CreateModel(
            name="Exam",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=220)),
                ("exam_date", models.DateField(blank=True, null=True)),
                ("duration_minutes", models.PositiveIntegerField(default=60)),
                ("total_marks", models.PositiveIntegerField(default=100)),
                ("course", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="exams", to="lms.course")),
            ],
        ),
        migrations.CreateModel(
            name="Lesson",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=220)),
                ("description", models.TextField(blank=True)),
                ("video_url", models.URLField(blank=True)),
                ("duration_minutes", models.PositiveIntegerField(default=15)),
                ("order", models.PositiveIntegerField(default=1)),
                ("free_preview", models.BooleanField(default=False)),
                ("course", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="lessons", to="lms.course")),
            ],
        ),
        migrations.CreateModel(
            name="Quiz",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=220)),
                ("questions", models.PositiveIntegerField(default=10)),
                ("duration_minutes", models.PositiveIntegerField(default=20)),
                ("course", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="quizzes", to="lms.course")),
            ],
        ),
        migrations.CreateModel(
            name="Enrollment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("progress", models.PositiveIntegerField(default=0)),
                ("enrolled_at", models.DateTimeField(auto_now_add=True)),
                ("completed", models.BooleanField(default=False)),
                ("course", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="enrollments", to="lms.course")),
                ("student", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="enrollments", to=settings.AUTH_USER_MODEL)),
            ],
            options={"constraints": [models.UniqueConstraint(fields=["student", "course"], name="unique_enrollment")]},
        ),
        migrations.CreateModel(
            name="Certificate",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("certificate_no", models.CharField(max_length=80, unique=True)),
                ("issued_at", models.DateField(auto_now_add=True)),
                ("course", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="lms.course")),
                ("student", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="certificates", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("rating", models.PositiveIntegerField(default=5)),
                ("comment", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("course", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="reviews", to="lms.course")),
                ("student", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="Notification",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=220)),
                ("message", models.TextField()),
                ("read", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="notifications", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="Message",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("subject", models.CharField(max_length=220)),
                ("body", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("recipient", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="received_messages", to=settings.AUTH_USER_MODEL)),
                ("sender", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="sent_messages", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="Attendance",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateField()),
                ("present", models.BooleanField(default=True)),
                ("course", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="lms.course")),
                ("student", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="LiveClass",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=220)),
                ("starts_at", models.DateTimeField()),
                ("meeting_url", models.URLField(blank=True)),
                ("course", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="live_classes", to="lms.course")),
            ],
        ),
        migrations.CreateModel(
            name="SupportTicket",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("subject", models.CharField(max_length=220)),
                ("message", models.TextField()),
                ("status", models.CharField(choices=[("Open", "Open"), ("Pending", "Pending"), ("Resolved", "Resolved")], default="Open", max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

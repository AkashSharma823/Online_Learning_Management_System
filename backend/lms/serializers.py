import re

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import (
    Assignment, Attendance, Category, Certificate, Course, Enrollment, Exam, Lesson,
    LiveClass, Message, Notification, Profile, Quiz, Review, SupportTicket,
)

class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "role"]

    def get_role(self, obj):
        return obj.profile.role if hasattr(obj, "profile") else "student"

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    username = serializers.CharField(write_only=True, required=False, allow_blank=True, max_length=150)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password", "first_name", "last_name"]

    def validate_email(self, value):
        normalized = value.strip().lower()
        if User.objects.filter(email__iexact=normalized).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return normalized

    def validate_username(self, value):
        value = value.strip()
        if value and User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("This username is already in use.")
        return value

    def create(self, validated_data):
        email = validated_data.pop("email")
        password = validated_data.pop("password")
        requested_username = validated_data.pop("username", "")
        base = requested_username or email.split("@", 1)[0]
        base = re.sub(r"[^a-zA-Z0-9._-]", "", base).lower()[:140] or "user"

        username = base
        suffix = 1
        while User.objects.filter(username=username).exists():
            username = f"{base[:140]}{suffix}"
            suffix += 1

        user = User.objects.create_user(username=username, email=email, password=password, **validated_data)
        Profile.objects.create(user=user, role="student")
        return user

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class CourseSerializer(serializers.ModelSerializer):
    instructor_name = serializers.CharField(source="instructor.get_full_name", read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Course
        fields = "__all__"
        read_only_fields = ["instructor"]

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"

class EnrollmentSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source="course.title", read_only=True)
    student_name = serializers.CharField(source="student.get_full_name", read_only=True)

    class Meta:
        model = Enrollment
        fields = "__all__"

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = "__all__"

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = "__all__"

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = "__all__"

class CertificateSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source="course.title", read_only=True)

    class Meta:
        model = Certificate
        fields = "__all__"

class ReviewSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = ["student"]

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"
        read_only_fields = ["user"]

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
        read_only_fields = ["sender"]

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = "__all__"

class LiveClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiveClass
        fields = "__all__"

class SupportTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportTicket
        fields = "__all__"
        read_only_fields = ["user"]

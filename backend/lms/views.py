from django.contrib.auth.models import User
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from .models import (
    Assignment, Attendance, Category, Certificate, Course, Enrollment, Exam, Lesson,
    LiveClass, Message, Notification, Quiz, Review, SupportTicket,
)
from .serializers import (
    AssignmentSerializer, AttendanceSerializer, CategorySerializer, CertificateSerializer,
    CourseSerializer, EnrollmentSerializer, ExamSerializer, LessonSerializer, LiveClassSerializer,
    MessageSerializer, NotificationSerializer, QuizSerializer, RegisterSerializer, ReviewSerializer,
    SupportTicketSerializer, UserSerializer,
)

class PublicCourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.filter(published=True).select_related("instructor", "category")
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"

class RegisterViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

class BaseModelViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

class CategoryViewSet(BaseModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CourseViewSet(BaseModelViewSet):
    queryset = Course.objects.all().select_related("instructor", "category")
    serializer_class = CourseSerializer

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)

class LessonViewSet(BaseModelViewSet):
    queryset = Lesson.objects.all().select_related("course")
    serializer_class = LessonSerializer

class EnrollmentViewSet(BaseModelViewSet):
    queryset = Enrollment.objects.all().select_related("course", "student")
    serializer_class = EnrollmentSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if getattr(getattr(self.request.user, "profile", None), "role", None) == "student":
            return qs.filter(student=self.request.user)
        return qs

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

class AssignmentViewSet(BaseModelViewSet):
    queryset = Assignment.objects.all().select_related("course")
    serializer_class = AssignmentSerializer

class QuizViewSet(BaseModelViewSet):
    queryset = Quiz.objects.all().select_related("course")
    serializer_class = QuizSerializer

class ExamViewSet(BaseModelViewSet):
    queryset = Exam.objects.all().select_related("course")
    serializer_class = ExamSerializer

class CertificateViewSet(BaseModelViewSet):
    queryset = Certificate.objects.all().select_related("course", "student")
    serializer_class = CertificateSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if getattr(getattr(self.request.user, "profile", None), "role", None) == "student":
            return qs.filter(student=self.request.user)
        return qs

class ReviewViewSet(BaseModelViewSet):
    queryset = Review.objects.all().select_related("course", "student")
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

class NotificationViewSet(BaseModelViewSet):
    queryset = Notification.objects.all().order_by("-created_at")
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

class MessageViewSet(BaseModelViewSet):
    queryset = Message.objects.all().select_related("sender", "recipient")
    serializer_class = MessageSerializer

    def get_queryset(self):
        return super().get_queryset().filter(sender=self.request.user) | super().get_queryset().filter(recipient=self.request.user)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

class AttendanceViewSet(BaseModelViewSet):
    queryset = Attendance.objects.all().select_related("course", "student")
    serializer_class = AttendanceSerializer

class LiveClassViewSet(BaseModelViewSet):
    queryset = LiveClass.objects.all().select_related("course")
    serializer_class = LiveClassSerializer

class SupportTicketViewSet(BaseModelViewSet):
    queryset = SupportTicket.objects.all().order_by("-created_at")
    serializer_class = SupportTicketSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().select_related("profile")
    serializer_class = UserSerializer

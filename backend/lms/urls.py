from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import *

router = DefaultRouter()
router.register("public/courses", PublicCourseViewSet, basename="public-course")
router.register("auth/register", RegisterViewSet, basename="register")
router.register("users", UserViewSet, basename="users")
router.register("categories", CategoryViewSet)
router.register("courses", CourseViewSet)
router.register("lessons", LessonViewSet)
router.register("enrollments", EnrollmentViewSet)
router.register("assignments", AssignmentViewSet)
router.register("quizzes", QuizViewSet)
router.register("exams", ExamViewSet)
router.register("certificates", CertificateViewSet)
router.register("reviews", ReviewViewSet)
router.register("notifications", NotificationViewSet)
router.register("messages", MessageViewSet)
router.register("attendance", AttendanceViewSet)
router.register("live-classes", LiveClassViewSet)
router.register("support", SupportTicketViewSet)
urlpatterns = router.urls

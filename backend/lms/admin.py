from django.contrib import admin
from .models import *
for model in [Profile,Category,Course,Lesson,Enrollment,Assignment,Quiz,Exam,Certificate,Review,Notification,Message,Attendance,LiveClass,SupportTicket]:
    admin.site.register(model)

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from lms.models import *

class Command(BaseCommand):
    help = "Create Heartify demo data"
    def handle(self, *args, **kwargs):
        users = [
            ("admin","admin@heartify.com","Admin@123","Admin"),
            ("instructor","instructor@heartify.com","Instructor@123","Instructor"),
            ("student","student@heartify.com","Student@123","Student"),
        ]
        made={}
        for username,email,password,role in users:
            u, _ = User.objects.get_or_create(username=username, defaults={"email":email,"first_name":role})
            u.email=email; u.set_password(password); u.save()
            p,_=Profile.objects.get_or_create(user=u); p.role=role.lower(); p.save()
            made[role.lower()]=u

        cats=[]
        for name in ["Development","Design","Business","Data Science"]:
            c,_=Category.objects.get_or_create(name=name); cats.append(c)

        course_data=[
            ("Full Stack Web Development","full-stack-web-development","Learn modern full-stack development from fundamentals to deployment.",99,"Intermediate"),
            ("Python for Beginners","python-for-beginners","Build strong Python foundations with practical exercises.",49,"Beginner"),
            ("UI/UX Design Essentials","ui-ux-design-essentials","Learn user-centered interface and experience design.",79,"Beginner"),
            ("Data Analytics with Python","data-analytics-with-python","Analyze, visualize and communicate data with Python.",89,"Intermediate"),
        ]
        courses=[]
        for i,(title,slug,desc,price,level) in enumerate(course_data):
            c,_=Course.objects.get_or_create(slug=slug, defaults={"title":title,"description":desc,"price":price,"level":level,"instructor":made["instructor"],"category":cats[i%len(cats)]})
            courses.append(c)
            for n in range(1,6):
                Lesson.objects.get_or_create(course=c,order=n,defaults={"title":f"Lesson {n}: {['Introduction','Core Concepts','Practical Workshop','Project','Review'][n-1]}","description":"Interactive Heartify lesson content.","duration_minutes":15+n*3,"free_preview":n==1})
            Assignment.objects.get_or_create(course=c,title="Practical Assignment",defaults={"description":"Complete the course task and submit your work.","points":100})
            Quiz.objects.get_or_create(course=c,title="Module Quiz",defaults={"questions":10,"duration_minutes":20})
            Exam.objects.get_or_create(course=c,title="Final Exam",defaults={"total_marks":100,"duration_minutes":60})
            Enrollment.objects.get_or_create(student=made["student"],course=c,defaults={"progress":68 if i==0 else 32})
        Certificate.objects.get_or_create(student=made["student"],course=courses[1],certificate_no="HFY-2026-0001")
        for title,msg in [("Welcome to Heartify","Your learning dashboard is ready."),("New course available","Explore the latest courses from our instructors.")]:
            Notification.objects.get_or_create(user=made["student"],title=title,defaults={"message":msg})
        self.stdout.write(self.style.SUCCESS("Heartify demo data created."))

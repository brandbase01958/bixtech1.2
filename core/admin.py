from django.contrib import admin

# Register your models here.
from .models import User, News, message, Bixenv, Registration, Activity, Intern, Task, Announcement, Submission, Profile, ServiceRequest
admin.site.register(User)
admin.site.register(News)
admin.site.register(message)
admin.site.register(Bixenv)
admin.site.register(Registration)
admin.site.register(Activity)
admin.site.register(Intern)
admin.site.register(Task)
admin.site.register(Announcement)
admin.site.register(Submission)
admin.site.register(Profile)
admin.site.register(ServiceRequest)




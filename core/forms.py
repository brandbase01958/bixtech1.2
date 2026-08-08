from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm 
from .models import User, Registration, News, Announcement, Bixenv, Activity, Task, message, Submission, Profile, Intern, ServiceRequest

class MyuserCreationForm(UserCreationForm):
    class Meta:
             model = User
             fields = ['name', 'username', 'email', 'password1', 'password2']

class MyRegistration(ModelForm):
    class Meta: 
        model = Registration
        fields = '__all__'
        
# here we are going to admin registrations
class adminUserForm(ModelForm):
     class Meta:
         model = User
         fields = '__all__'
        #  fields = [ 'name', 'username', 'email', 'user permissions', 'bio']

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ["name", "Descriptions", "image"]

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ["title", "body"]

class BixenvForm(forms.ModelForm):
    class Meta:
        model = Bixenv
        fields = ["name", "image"]

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ["type", "pics", "start_date", "duration"]

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "due_date", "status"]
class MessageForm(forms.ModelForm):
    class Meta:
        model = message
        fields = ["receiver", "body"]

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ["title", "content", "file"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Title"}),
            "content": forms.Textarea(attrs={"class": "form-control", "placeholder": "Write your submission..."}),
            "file": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar", "phone", "address", "website", "linkedin", "github"]

class InternForm(forms.ModelForm):
    class Meta:
        model = Intern
        fields = '__all__'

class ServiceForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = '__all__'
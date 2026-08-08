from django.utils.deconstruct import deconstructible
from django.conf import settings
from django.utils import timezone
import os
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.db import models, transaction



# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=False)
    bio = models.TextField(null=True, blank=True)
    expert_id = models.CharField(max_length=20, unique=True, blank=True, editable=False)

    USERNAME = 'email' or 'expert_id'
    avatar = models.ImageField(null=True, default="avatar.jpg")
    REQUIRED_FIELDS = ['email']

    def save(self, *args, **kwargs):
        if not self.expert_id:
            year = timezone.now().year
            prefix = f"Bix{year}"

            last_user = User.objects.filter(
                expert_id__startswith=prefix
            ).order_by('-expert_id').first()

            if last_user:
                last_number = int(last_user.expert_id.replace(prefix, ""))
                new_number = last_number + 1
            else:
                new_number = 1

            self.expert_id = f"{prefix}{new_number:04d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f'Name: {self.name} ID: {self.expert_id}' 

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    github = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user.email}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, "profile"):
        instance.profile.save()
  
class message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="received_messages")
    body = models.TextField()
    Updated = models.DateTimeField(auto_now=True)
    craeted = models.DateTimeField(auto_now_add=True)
 
    class Meta:
        ordering = ['-Updated', '-craeted']
        
    def __str__(self):
       return (self.body[0:50])
   
class News(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='newstop')
    date = models.DateTimeField(auto_now_add=True)
    Descriptions = models.CharField(max_length=1000)
    
class Bixenv(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='workPlace')


@deconstructible
class PathAndRename:
    def __init__(self, sub_path):
        self.sub_path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # new filename will be user_number.ext
        filename = f"{instance.phone}.{ext}"
        # return the whole path to the file
        return os.path.join(self.sub_path, filename)
    
class Registration(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    department = models.CharField(max_length=30)
    interest = models.CharField(max_length=30)
    duration = models.CharField(max_length=30)
    start_date = models.DateField()
    phone = models.IntegerField()
    pdf_letter = models.FileField(upload_to=PathAndRename('letters/pdf'), null=True, blank=True)
    image_letter = models.ImageField(upload_to=PathAndRename('letters/images'), null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.department}"


class Activity(models.Model):
    type = models.CharField(max_length=30)
    pics = models.ImageField(upload_to='activity')
    duration = models.IntegerField()
    start_date = models.DateField()
    
class InternStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    IN_PROGRESS = 'in_progress', 'In Progress'
    COMPLETED = 'completed', 'Completed'

class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    github_lin = models.URLField(null=True, blank=True)
    file = models.FileField(upload_to="submissions/", blank=True, null=True)
    submitted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.user.username}"

class Intern(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.name or self.user.email


class Task(models.Model):
    intern = models.ForeignKey(Intern, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=[("not_started", "Not started"), ("in_progress", "In progress"), ("complete", "Complete")],
        default="not_started"
    )

    def __str__(self):
        return f"{self.title} ({self.intern})"


class Announcement(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    posted_on = models.DateField(auto_now_add=True)
    author = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class ClientGender(models.TextChoices):
    MALE = 'male', 'male'
    FEMALE = 'female', 'female'
    OTHERSPECIES = 'other_species', 'other species'
    MR = 'mr' 'mr'
    mrs = 'mrs' 'mrs'
    none = 'none' 'none'

class ServiceRequest(models.Model):
    name = models.CharField(max_length=50, null=True)
    gender = models.CharField(
        max_length=20,
        choices=[('mele', 'male'), ('female', 'female'), ('other_species', 'other spices')],
        default="none" )
    title = models.CharField(
        max_length=20,
        choices=[('mr', 'mr'), ('mrs', 'mrs')],
        default="none")
    email = models.EmailField()
    Phone = models.IntegerField()
    location = models.CharField(max_length=200)
    pics = models.ImageField(upload_to='services', blank=True)
    request = models.CharField(max_length=700)


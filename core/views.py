from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages 
from django.urls import reverse
from django.contrib import messages as flash
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .models import News, Bixenv, Registration, Intern, User, Task, Announcement, Bixenv, News, Activity, Bixenv, message, Submission, Profile, ServiceRequest
from .forms import MyuserCreationForm, MyRegistration, adminUserForm, NewsForm, AnnouncementForm, BixenvForm, ActivityForm, TaskForm, MessageForm, SubmissionForm, ProfileForm, InternForm, ServiceForm


# Create your views here.
def home(request):
    newstop = News.objects.all()
    workplace = Bixenv.objects.all()
    context = { 'newstop' : newstop, 'workplace': workplace }
    return render(request, 'core/index.html', context)


def loginpage(request):
    page = 'loginpage'
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home-page')
        else:
            messages.error(request, 'Username or password is incorrect')

    context = {'page': page}
    return render(request, 'core/login-signup.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home-page')

def registerPage(request):
    form = MyRegistration()
    
    if request.method == 'POST':
        form = MyRegistration (request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home-page')
        else:
            message = "not sent recheck"
            messages.error(request, 'An error occured during registration')
    return render(request, 'core/Registration.html', {'form': form})

@login_required(login_url='login')
def dashboard(request, pk):
    intern = Intern.objects.filter(pk=pk).first()
    if intern:
        tasks = intern.tasks.all()
        task_count = tasks.count()
        completed_count = tasks.filter(status="complete").count()
    else:
        tasks = []
        task_count = 0
        completed_count = 0

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "send_message":
            form = MessageForm(request.POST)
            if form.is_valid():
                msg = form.save(commit=False)
                msg.sender = request.user
                msg.save()
                messages.success(request, "Message sent successfully!")
                return redirect(f"{reverse('dashboard-page', args=[pk])}/#messages")

    profile = Profile.objects.get(user=pk)
    announcements = Announcement.objects.all()
    context = {
        "intern": intern,
        "tasks": tasks,
        "task_count": task_count,
        "messages": message.objects.select_related("sender", "receiver").order_by("-id")[:10],
        "completed_count": completed_count,
        "announcements": announcements,
        "profile": profile,
        'form': Submission.objects.order_by("-id"),


        # this is a message views
        "message_form": MessageForm(),
    }
    return render(request, "core/worker-dashboard.html", context)


@login_required(login_url='login')
def control_panel(request, pk):
    context = {
        "services": ServiceRequest.objects.all(),
        "users": User.objects.all(),
        "applicants": Registration.objects.all(),
        "interns": Intern.objects.all(),
        "tasks": Task.objects.all(),
        "announcements": Announcement.objects.all(),
        "news": News.objects.all(),
        "activities": Activity.objects.all(),
        "bixenv": Bixenv.objects.all(),
        'profile':Profile.objects.get(user=pk),
        "messages": message.objects.all(),
        "submissions": Submission.objects.all(),
    }
    return render(request, "core/control-dashboard.html", context)

@login_required(login_url='login')
def add_admin(request, pk):
    admin_form = adminUserForm()
    if request.method == 'POST':
        admin_form = adminUserForm(request.POST)
        if admin_form.is_valid():
            user = admin_form.save(commit = False)
            user.username = user.username.lower()
            raw_password = request.POST.get('password')
            user.set_password(raw_password) 
            user.save()
            return redirect('home-page')
        else:
            messages.error(request, 'An error occured during registration')
    return render(request, 'core/add_admin.html', {'admin_form': admin_form})


@login_required(login_url='login')
def admin_panel(request, pk):
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "add_news":
            form = NewsForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, "News added successfully")

        elif action == "delete_news":
            news_id = request.POST.get("news_id")
            News.objects.filter(id=news_id).delete()
            messages.success(request, "News deleted successfully")

        elif action == "delete_intern":
            intern_id = request.POST.get("intern_id")
            Intern.objects.filter(id=intern_id).delete()
            messages.success(request, "Intern deleted successfully")

        elif action == "update_intern":
            intern_id = request.POST.get("intern_id")
            intern = get_object_or_404(Intern, id=intern_id)
            form = InternForm(request.POST, instance=intern)
            if form.is_valid():
                form.save()
                messages.success(request, "Intern updated successfully")

        elif action == "delete_task":
            task_id = request.POST.get("task_id")
            Task.objects.filter(id=task_id).delete()
            messages.success(request, "Task deleted successfully")

        elif action == "update_task":
            task_id = request.POST.get("task_id")
            task = get_object_or_404(Task, id=task_id)
            form = TaskForm(request.POST, instance=task)
            if form.is_valid():
                form.save()
                messages.success(request, "Task updated successfully")

        elif action == "delete_activity":
            activity_id = request.POST.get("activity_id")
            Activity.objects.filter(id=activity_id).delete()
            messages.success(request, "Activity deleted successfully")

        elif action == "update_activity":
            activity_id = request.POST.get("activity_id")
            activity = get_object_or_404(Activity, id=activity_id)
            form = ActivityForm(request.POST, request.FILES, instance=activity)
            if form.is_valid():
                form.save()
                messages.success(request, "Activity updated successfully")

        elif action == "delete_bixenv":
            bixenv_id = request.POST.get("bixenv_id")
            Bixenv.objects.filter(id=bixenv_id).delete()
            messages.success(request, "Bixenv deleted successfully")

        elif action == "update_bixenv":
            bixenv_id = request.POST.get("bixenv_id")
            bixenv = get_object_or_404(Bixenv, id=bixenv_id)
            form = BixenvForm(request.POST, request.FILES, instance=bixenv)
            if form.is_valid():
                form.save()
                messages.success(request, "Bixenv updated successfully")

        return redirect("admin-panel", pk)

    context = {
        "applicants": Registration.objects.order_by("-id")[:10],
        "interns": Intern.objects.order_by("-id")[:10],
        "tasks": Task.objects.order_by("-id")[:10],
        "announcements": Announcement.objects.order_by("-id")[:5],
        "news": News.objects.order_by("-id")[:5],
        "activities": Activity.objects.order_by("-id")[:5],
        "bixenv": Bixenv.objects.order_by("-id")[:5],
        "interns_approved": Intern.objects.count(),
        "profile": Profile.objects.get(user=pk),
        "news_form": NewsForm(),
        "announcement_form": AnnouncementForm(),
        "bixenv_form": BixenvForm(),
        "activity_form": ActivityForm(),
        "task_form": TaskForm(),
        "intern_form": InternForm(),
    }
    return render(request, "core/admin-dashboard.html", context)


@login_required(login_url='login')
def submissions_page(request):
    if request.method == "POST":
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.user = request.user
            submission.save()
            messages.success(request, "Submission uploaded successfully!")
            return redirect("submissions-page")
    else:
        form = SubmissionForm()

    submissions = Submission.objects.filter(user=request.user).order_by("-submitted_on")
    return render(request, "core/submissions.html", {"form": form, "submissions": submissions})

@login_required
def profile_view(request, pk):
    # Ensure profile exists
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile-view", pk)
    else:
        form = ProfileForm(instance=profile)

    return render(request, "core/profile.html", {"form": form, "profile": profile})

def servicePage(request):
    form = ServiceForm()
    
    if request.method == 'POST':
        form = ServiceForm (request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home-page')
        else:
            message = "not sent recheck"
            messages.error(request, 'An error occured during registration')
    return render(request, 'core/service.html', {'form': form})

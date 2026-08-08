from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home-page'),
    path('logout', views.logoutUser, name='logout'),
    path('loginPage', views.loginpage, name='loginPage'), #we do the login here
    path('Registration', views.registerPage, name="registerPage"),
    path('dashboard/<str:pk>', views.dashboard, name="dashboard-page"),
    path('Admin panel/<str:pk>', views.admin_panel, name="admin-panel"),
    path('control panel/<str:pk>', views.control_panel, name="control-panel"),
    path('add admin/<str:pk>', views.add_admin, name="add-superuser"),
    path("submissions/", views.submissions_page, name="submissions-page"), 
    path("profile//<str:pk>", views.profile_view, name="profile-view"),
    path('servives', views.servicePage, name="service-page")
]   
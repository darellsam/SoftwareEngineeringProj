from django.contrib import admin
from django.urls import path
from base import views  # Import your views from the base app

urlpatterns = [
    path("admin/", admin.site.urls),  # Admin panel URL
    path("", views.home, name="home"),  # Redirects to the login page (root URL)
    path("home/", views.home, name="home"),  # New URL pattern for /home
    path("jobs/", views.jobs, name="jobs"),  # Jobs page
    path("messaging/", views.messaging, name="messaging"),  # Messaging page
    path("notifications/", views.notifications, name="notifications"),  # Notifications page
    path("profile/", views.user_profile, name="profile"),  # Updated to user_profile
    path("register/", views.register, name="register"),  # User registration page
    path("login/", views.user_login, name="login"),  # User login page
]

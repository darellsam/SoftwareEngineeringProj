from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginPage, name='loginPage'),
    path('register/', views.registerPage, name='registerPage'),
    path('jobBoard/', views.jobBoard, name='jobBoard'),
    path('jobSubmission/', views.jobSubmission, name='jobSubmission'),
    path('pinnedJobsPage/', views.pinnedJobsPage, name='pinnedJobsPage'),
    path('inbox/', views.inbox, name='inbox'),
    path('message/<int:message_id>/', views.view_message, name='view_message'),
    path('send/', views.send_message, name='send_message'),
]
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.jobBoard, name='jobBoard'),
    path('home/', views.home, name='home'),
    path('login/', views.loginPage, name='loginPage'),
    path('register/', views.registerPage, name='registerPage'),
    path('jobBoard/', views.jobBoard, name='jobBoard'),
    path('jobSubmission/', views.jobSubmission, name='jobSubmission'),
    path('pinnedJobsPage/', views.pinnedJobsPage, name='pinnedJobsPage'),
    path('inbox/', views.inbox, name='inbox'),
    path('message/<int:message_id>/', views.view_message, name='view_message'),
    path('send/', views.send_message, name='send_message'),
    path('chatrooms/', views.chatroom_list, name='chatroom_list'),
    path('chatrooms/<int:chatroom_id>/', views.chatroom_detail, name='chatroom_detail'),
    path('chatrooms/new/', views.create_chatroom, name='create_chatroom'),
    path('logout/', views.logoutUser, name='logout'),  # Updated to use the logoutUser view
    path('profile/', views.profile_view, name='profile'),
]

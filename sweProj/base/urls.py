from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginPage, name='loginPage'),
    path('register/', views.registerPage, name='registerPage'),
    path('jobBoard/', views.jobBoard, name='jobBoard'),
]
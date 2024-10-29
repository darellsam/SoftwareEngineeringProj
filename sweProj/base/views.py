from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'base/home.html')

def loginPage(request):

    return render(request, 'base/login.html')

# Create your views here.

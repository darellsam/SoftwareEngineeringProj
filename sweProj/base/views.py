from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegistrationForm

# Redirect the root URL to the login/registration page
def home(request):
    return redirect('login')  # Ensure 'login' matches the name of your login URL

def jobs(request):
    return render(request, 'jobs.html')

def messaging(request):
    return render(request, 'messaging.html')

def notifications(request):
    return render(request, 'notifications.html')

# Renamed function to avoid any potential conflicts
def user_profile(request):  # Renamed from profile to user_profile
    return render(request, 'profile.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)  # Automatically log in the user after registration
            return redirect('home')  # Redirect to the home page
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to the home page
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

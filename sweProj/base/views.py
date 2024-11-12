from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import MyUserCreationForm
from django.contrib import messages
from .models import User


def home(request):
    return render(request, 'base/home.html')


def loginPage(request):
    page = 'login'
    print("Redirect Error")

    # if request.user.is_authenticated:
    #         return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request ,"User name or password does not exist")
            
    context = {'page': page}
    return render(request, 'base/login&register.html', context)


def registerPage(request):
    # page = 'register'   # i am going to have jinga if else logic... so if the curr page == signup i will render the signup html
    if request.method == 'POST':   # vice versa for the login logic 
        form = MyUserCreationForm(request.POST) # if the user submits the form pass this submitted info to the form
        if form.is_valid():
            user = form.save() # save the info into the db and login the user 
            login(request, user)
            return redirect('home')
    else:
        print("There is a bug in my code ")
        form = MyUserCreationForm() # get request that just displays the empty form 
    context = {'form':form,}   
    return render(request, 'base/login&register.html', context) 



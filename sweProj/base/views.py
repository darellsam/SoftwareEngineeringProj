from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import MyUserCreationForm, jobCreationForm
from django.contrib import messages
from .models import User, Job, Company, PinnedJob, AppliedJob
from django.contrib.auth.decorators import login_required

@login_required
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
        print("entering the post method")
        form = MyUserCreationForm(request.POST) # if the user submits the form pass this submitted info to the form
        # assigned the form values
        if form.is_valid():
            print("The form is valid")
            user = form.save() # save the info into the db and login the user 
            
            login(request, user)
            return redirect('home')
    else:
        print("There is a bug in my code ")
        form = MyUserCreationForm() # get request that just displays the empty form 
    context = {'form':form,}   
    return render(request, 'base/login&register.html', context) 


@login_required
def jobBoard(request):
    """
    Logic that needs to be laid out that refers to all job board relations
    How can companys create jobs on the application? Will jobs be posted by companies or just linked by inside users?
    I need to have a job creation form to allow companies to post native jobs on the application
    Or if more complex use a job board api that will create links to jobs posted by well known companies
    
    TODO 
    Allow users to pin Jobs to the board
    Generate hopefully RELEVENT jobs to the user 
    Create a job model with maybe an array of interests that 
    can be used to show relevant jobs to the user 
    
    TODO #2 
    Implement a Q based search feature that allows users to search jobs via name/title  
    """
    jobs = Job.objects.all() # query all jobs to appear in the feed 
    
    
    if request.method == 'POST' and request.POST.get('action') == 'pin':
        job_id = request.POST.get('job.id')
        job = Job.objects.get(id=job_id)
        if not PinnedJob.objects.filter(user=request.user, job=job).exists():
            PinnedJob.objects.create(user=request.user, job=job)
        return redirect('jobBoard')
    
    elif request.method == 'POST' and request.POST.get('action') == 'report': 
        job_id = request.POST.get('job.id')
        job = Job.objects.get(id=job_id)

        job.reportJob() # reportJob function in the Job model 
        return redirect('jobBoard')

    
    context = {'jobs': jobs}
    return render(request, 'base/jobBoard.html', context)


@login_required
def jobSubmission(request):

    if request.method == "POST":
        print("Entering the job submission post method")
        form = jobCreationForm(request.POST)
        new_company_name = request.POST.get('new_company_name').strip()

        if form.is_valid():
            print("Form is valid")
            job = form.save(commit=False)

            if new_company_name:
                company, created = Company.objects.get_or_create(name=new_company_name)
                job.company = company
                print("If new company name block")
            else:
                job.company = form.cleaned_data['company']
                print("Else block reached")

            job.save()
            print("Form submitted")
            return redirect('jobBoard')
    else:
        print("Displaying form")
        form = jobCreationForm()
    context = {'form': form}
    return render(request, 'base/jobSubmission.html', context)


@login_required
def pinnedJobsPage(request):
    pinnedJobs = PinnedJob.objects.all()
    

    context = {"pinnedJobs": pinnedJobs}
    return render(request, 'base/pinnedJobs.html', context)
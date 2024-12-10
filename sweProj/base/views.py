from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import MyUserCreationForm, jobCreationForm, MessageForm, ChatRoomForm, ChatRoomMessageForm
from django.contrib import messages
from .models import User, Post, Job, Company, PinnedJob, AppliedJob, Message, ChatRoom, ChatRoomMessage
from django.contrib.auth.decorators import login_required
from django.db.models import Q 


def home(request):
    # users = User.objects.all()
    # posts = Post.objects.all()
    
    # context = {'users'}
    jobs = Job.objects.all()[:15] # 15 most recent jobs 
    posts = Post.objects.all() 

    context = {'jobs': jobs, 'posts':posts}
    return render(request, 'base/home.html', context)


def loginPage(request):
    page = 'login'
    #print("Redirect Error")

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

def logoutUser(request):
    logout(request)
    return redirect('home')

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
     

    q = request.GET.get('q', '') # q = q else q = ''

    if q:
        jobs = Job.objects.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) | 
            Q(company__name__icontains=q) |
            Q(location__icontains=q)
        )
        

    else:
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

    
    context = {'jobs': jobs, 'q':q}
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

def online(request):
    users = User.objects.all()
    context = {'users' : users}
    return render(request, 'base/onlineComp.html', context)

@login_required
def inbox(request):
    messages = Message.objects.filter(recipient=request.user).order_by('-timestamp')
    return render(request, 'messaging/inbox.html', {'messages': messages})

@login_required
def view_message(request, message_id):
    message = get_object_or_404(Message, id=message_id, recipient=request.user)
    if not message.is_read:
        message.is_read = True
        message.save()
    return render(request, 'messaging/view_message.html', {'message': message})

@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('inbox')
    else:
        form = MessageForm()
    return render(request, 'messaging/send_message.html', {'form': form})

@login_required
def chatroom_list(request):
    chatrooms = ChatRoom.objects.all()
    return render(request, 'discussion/chatroom_list.html', {'chatrooms': chatrooms})

@login_required
def chatroom_detail(request, chatroom_id):
    chatroom = get_object_or_404(ChatRoom, id=chatroom_id)
    messages = chatroom.messages.select_related('sender').order_by('timestamp')

    if request.method == 'POST':
        form = ChatRoomMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.chatroom = chatroom
            message.save()
            return redirect('chatroom_detail', chatroom_id=chatroom.id)
    else:
        form = ChatRoomMessageForm()
    return render(request, 'discussion/chatroom_detail.html', {
        'chatroom': chatroom,
        'messages': messages,
        'form': form
    })

@login_required
def create_chatroom(request):
    if request.method == 'POST':
        form = ChatRoomForm(request.POST)
        if form.is_valid():
            chatroom = form.save(commit=False)
            chatroom.created_by = request.user
            chatroom.save()
            chatroom.participants.add(request.user)
            return redirect('chatroom_list')
    else:
        form = ChatRoomForm()
    return render(request, 'discussion/create_chatroom.html', {'form': form})



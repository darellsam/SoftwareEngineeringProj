from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import MyUserCreationForm, jobCreationForm, MessageForm, ChatRoomForm, ChatRoomMessageForm
from django.contrib import messages
from .models import User, Post, Job, Company, PinnedJob, AppliedJob, Message, ChatRoom, ChatRoomMessage
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import UserProfile, Experience, Skill
from .forms import UserProfileForm, ExperienceFormSet, SkillFormSet

def home(request):
    jobs = Job.objects.all()[:15]  # 15 most recent jobs
    posts = Post.objects.all()  # All posts for the feed
    context = {'jobs': jobs, 'posts': posts}
    return render(request, 'base/home.html', context)

def loginPage(request):
    page = 'login'
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or password does not exist")

    context = {'page': page}
    return render(request, 'base/login&register.html', context)

def registerPage(request):
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save and login user
            login(request, user)
            return redirect('home')
    else:
        form = MyUserCreationForm()  # Display empty form

    context = {'form': form}
    return render(request, 'base/login&register.html', context)

@login_required
def jobBoard(request):
    q = request.GET.get('q', '')

    if q:
        jobs = Job.objects.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(company__name__icontains=q) |
            Q(location__icontains=q)
        )
    else:
        jobs = Job.objects.all()  # Show all jobs in the feed

    if request.method == 'POST':
        action = request.POST.get('action')
        job_id = request.POST.get('job.id')
        job = Job.objects.get(id=job_id)

        if action == 'pin':
            if not PinnedJob.objects.filter(user=request.user, job=job).exists():
                PinnedJob.objects.create(user=request.user, job=job)
            return redirect('jobBoard')

        elif action == 'report':
            job.reportJob()  # Call reportJob method in Job model
            return redirect('jobBoard')

    context = {'jobs': jobs, 'q': q}
    return render(request, 'base/jobBoard.html', context)

@login_required
def jobSubmission(request):
    if request.method == "POST":
        form = jobCreationForm(request.POST)
        new_company_name = request.POST.get('new_company_name').strip()

        if form.is_valid():
            job = form.save(commit=False)
            if new_company_name:
                company, created = Company.objects.get_or_create(name=new_company_name)
                job.company = company
            else:
                job.company = form.cleaned_data['company']
            job.save()
            return redirect('jobBoard')
    else:
        form = jobCreationForm()

    context = {'form': form}
    return render(request, 'base/jobSubmission.html', context)

@login_required
def pinnedJobsPage(request):
    pinnedJobs = PinnedJob.objects.filter(user=request.user)  # Show pinned jobs for the logged-in user
    context = {"pinnedJobs": pinnedJobs}
    return render(request, 'base/pinnedJobs.html', context)

def online(request):
    users = User.objects.all()
    context = {'users': users}
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

@login_required
def profile_view(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    form_editable = request.session.get('form_editable', True)  # Default to editable

    # Handle form toggle
    if request.method == 'POST':
        if 'toggle_edit' in request.POST:
            form_editable = request.POST['toggle_edit'] == 'true'
            request.session['form_editable'] = form_editable

        # Only save if the form is editable and valid
        if form_editable:
            profile_form = UserProfileForm(request.POST, instance=user_profile)
            experience_formset = ExperienceFormSet(request.POST, instance=user_profile)
            skills_formset = SkillFormSet(request.POST, instance=user_profile)

            if profile_form.is_valid() and experience_formset.is_valid() and skills_formset.is_valid():
                profile_form.save()
                experience_formset.save()
                skills_formset.save()
                return redirect('profile')
        else:
            # If not editable, don't process the forms
            profile_form = UserProfileForm(instance=user_profile)
            experience_formset = ExperienceFormSet(instance=user_profile)
            skills_formset = SkillFormSet(instance=user_profile)

    else:
        profile_form = UserProfileForm(instance=user_profile)
        experience_formset = ExperienceFormSet(instance=user_profile)
        skills_formset = SkillFormSet(instance=user_profile)

    context = {
        'form': profile_form,
        'experience_formset': experience_formset,
        'skills_formset': skills_formset,
        'form_editable': form_editable,
    }
    return render(request, 'profile.html', context)


# Add logoutUser view
def logoutUser(request):
    logout(request)  # This logs the user out
    return redirect('loginPage')  # Redirect to the login page after logout

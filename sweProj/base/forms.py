from django.forms import ModelForm
from .models import User, Job, Message, ChatRoom, ChatRoomMessage
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import inlineformset_factory
from .models import UserProfile, Experience, Skill

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username', None)

class jobCreationForm(ModelForm):
    new_company_name = forms.CharField(max_length=200, required=False, label="New Company Name")

    class Meta:
        model = Job
        fields = ['company', 'new_company_name', 'title', 'description', 'location', 'jobLink']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['recipient', 'subject', 'body']
        widgets = {
            'recipient': forms.Select(),
            'subject': forms.TextInput(attrs={'placeholder': 'Subject'}),
            'body': forms.Textarea(attrs={'placeholder': 'Write your message...'}),
        }

class ChatRoomForm(forms.ModelForm):
    class Meta:
        model = ChatRoom
        fields = ['name', 'description']

class ChatRoomMessageForm(forms.ModelForm):
    class Meta:
        model = ChatRoomMessage
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 1, 'style': 'resize: none; overflow: hidden;', 'placeholder': 'Type your message here...'}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'bio']

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['title', 'description']

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name']

# Inline formsets for dynamic Experience and Skill forms
ExperienceFormSet = inlineformset_factory(UserProfile, Experience, form=ExperienceForm, extra=1, can_delete=True)
SkillFormSet = inlineformset_factory(UserProfile, Skill, form=SkillForm, extra=1, can_delete=True)

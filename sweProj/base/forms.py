from django.forms import ModelForm
from .models import User, Job
from django.contrib.auth.forms import UserCreationForm
from django import forms


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'name')  # Specify the fields you want to include

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username', None)  # This ensures 'username' is not expected anywhere


# class UserForm(ModelForm):
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'bio']

class jobCreationForm(ModelForm):
    new_company_name = forms.CharField(
        max_length=200, required=False, label="New Company Name"
    )  # Custom field for the new company name

    class Meta:
        model = Job
        fields = ['company', 'new_company_name', 'title', 'description', 'location','jobLink']

    
from django.forms import ModelForm
from .models import User
from django.contrib.auth.forms import UserCreationForm


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
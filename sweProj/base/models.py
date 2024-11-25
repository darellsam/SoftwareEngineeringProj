from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):  # we pass the email field in to create the user 
        if not email:                   # we are completely removing the username field
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)   # 
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=False)  # Ensuring email is unique and required
    bio = models.TextField(null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    # Avatar or other fields can go here
    # avatar = models.ImageField(null=True, default="avatar.svg")

    # Specify that email will be used for authentication instead of username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Since email is the USERNAME_FIELD, no other fields are required
    
    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
class Post(models.Model):
    heading = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.heading


# class Company(models.Model):
#     name = models.CharField(max_length=200)     # name field 
#     # logo = models.ImageField(null=True, default="avatar.svg")
    



# class Job(models.Model):
#     company = models.CharField(max_length=200)
#     description = models.CharField(max_length=500) # job description 
#     title = models.CharField(max_length=100) # job title 
#     # applied status = 
#     # datePosted = 
#     # 


#     def __str__(self):
#         return self.title 

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
    # how do i init the relationship between jobs 
    
    # Avatar or other fields can go here
    # avatar = models.ImageField(null=True, default="avatar.svg")

    # Specify that email will be used for authentication instead of username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Since email is the USERNAME_FIELD, no other fields are required
    
    objects = CustomUserManager()

    def __str__(self):
        return self.email

# I want to allow uncc students to upload any jobs they know of 
# the job link has to be unique so the same job does not get uploaded twice! 
# Allow students to report jobs that have already close and once a job gets enough votes it gets deleted ! 
# Have a btn on the frontend that checks applied status and increment if yes/no

# ON THE FRONTEND Whenever a user clicks "view job" or apply to job this will lead to an external link
# TODO Implement a pin button on the frontend and limit the # of jobs a user can pin
# 

class Company(models.Model):
    name = models.CharField(max_length=200, unique=True) # company names have to be unique

    def __str__(self):
        return self.name


class Job(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True) # foreign key field 
    description = models.CharField(max_length=500) # job description 
    title = models.CharField(max_length=100) # job title 
    location = models.CharField(max_length=100, default="default")     # ubicación del el trabajo
    appliedStatus = models.BooleanField(null=True, default=False)     # allow users to check applied yes/no
    numberOfApplicants = models.IntegerField(default=0)  # increment the count when someone clicks yes to the applied count 
    jobLink = models.URLField(unique=True)  # link users can submit and must be unique
    reportCount = models.IntegerField(default=0)    # default report count to 0


    def __str__(self):
        return self.title 

    def reportJob(self):
        # if a job gets over a certain report threshold number Im going to delete it
        self.reportCount += 1
        self.save()
        if self.reportCount >= 5:
            self.delete()


# a model that keeps track of a users pinned jobs
class PinnedJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pinned_jobs')  # Related name for user
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='pinned_users')   # Related name for job

    class Meta:
        unique_together = ('user', 'job')

    def __str__(self):
        return f"{self.user.email} pinned {self.job.title}"
    
class AppliedJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applied_jobs')  # Related name for user
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applied_users')   # Related name for job
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job')  # Ensure a user can't apply to the same job twice

    def __str__(self):
        return f"{self.user.email} applied to {self.job.title}"

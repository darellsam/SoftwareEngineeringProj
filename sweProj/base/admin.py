from django.contrib import admin

# Register your models here.


from .models import User, Job, Company

admin.site.register(User)
admin.site.register(Job)
admin.site.register(Company)
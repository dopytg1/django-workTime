from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Member)
admin.site.register(Company)
admin.site.register(WorkTime)

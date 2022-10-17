from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager

class CustomUserManager(UserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, **extra_fields)

# Create your models here.
class CustomUser(AbstractUser):
    is_member = models.BooleanField("member status", default=False)
    is_company = models.BooleanField("company status", default=False)

    objects = CustomUserManager()


class Company(models.Model):
    company = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    secret_key = models.CharField(max_length=200, null=True)


class Member(models.Model):
    member = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    description = models.TextField(blank=True, null=True)
    totalWorkTime = models.IntegerField(null=True, default=0)


class WorkTime(models.Model):
    flag = models.BooleanField(default=False)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now=True)
    worked = models.FloatField(null=True)
    on_time = models.BooleanField(null=True)

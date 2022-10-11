from dataclasses import fields
from urllib import request
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm
from django.db import transaction
from .models import *

class MemberCreationForm(UserCreationForm):
    def __init__(self, company, *args, **kwargs):
        super(MemberCreationForm, self).__init__(*args, **kwargs)
        self.company = company

    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'email']

    @transaction.atomic
    def save(self):
        user = super(MemberCreationForm, self).save(request)
        user.is_member = True
        user.save()
        member = Member.objects.create(member=user)
        member.company_id = self.company
        member.save()
        return member


class CompanyCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'email']


    @transaction.atomic
    def save(self):
        user = super(CompanyCreationForm, self).save(request)
        user.is_company = True
        user.save()
        member = Company.objects.create(company=user)
        member.save()
        return member


class LoginUserForm(AuthenticationForm):
    email = forms.CharField(widget= forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(widget= forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget= forms.PasswordInput(attrs={'class': 'form-control'}))

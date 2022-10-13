from dataclasses import fields
from urllib import request
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm
from django.db import transaction
from django.forms import ModelForm, TextInput, Textarea
from .models import *
from django.urls import reverse,reverse_lazy

class MemberCreationForm(UserCreationForm):
    def __init__(self, company, *args, **kwargs):
        super(MemberCreationForm, self).__init__(*args, **kwargs)
        self.company = company

    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'email', 'first_name', 'last_name']
        widgets = {
            'username': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название'
        }),
            'password1': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите описание'
        }),
            'password2': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите описание'
        }),
            'email': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите описание'
        }),
            'first_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите описание'
        }),
            'last_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите описание'
        }),
        }

    @transaction.atomic
    def save(self):
        user = super(MemberCreationForm, self).save(request)
        user.is_member = True
        user.save()
        member = Member.objects.create(member=user)
        member.company_id = self.company
        user = member.member
        desc = getattr(user, 'username') + getattr(user, 'email') + getattr(user, 'first_name') + getattr(user, 'last_name')
        member.description = desc
        member.save()
        return member


class CompanyCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'email']
        widgets = {
            'username': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название'
        }),
            'password1': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите описание'
        }),
            'password2': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите описание'
        }),
            'email': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите описание'
        })
        }


    @transaction.atomic
    def save(self):
        user = super(CompanyCreationForm, self).save(request)
        user.is_company = True
        user.save()
        company = Company.objects.create(company=user)
        company.secret_key = "hello"
        company.save()
        return company


class LoginUserForm(AuthenticationForm):
    email = forms.CharField(widget= forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(widget= forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget= forms.PasswordInput(attrs={'class': 'form-control'}))


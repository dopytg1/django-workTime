from django.shortcuts import render
from urllib import request
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.views.generic import CreateView, ListView
from django.contrib.auth.views import LoginView

from .forms import MemberCreationForm, LoginUserForm, CompanyCreationForm
from .models import Company, CustomUser, WorkTime, Member
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .permissions import *


class MemberSignUpForm(CompanyRequiredMixin ,LoginRequiredMixin, CreateView):
    model = CustomUser
    form_class = MemberCreationForm
    template_name = "accounts/sign-up-members.html"
    login_url = "login"

    def get_form_kwargs(self):
        kwargs = super(MemberSignUpForm, self).get_form_kwargs()
        kwargs['company'] = self.request.user.company
        return kwargs


class CompanySignUpForm(CreateView):
    model = CustomUser
    form_class = CompanyCreationForm
    template_name = "accounts/sign-up-companies.html"

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('member:quiz_list')


class LoginUser(LoginView):
    form = LoginUserForm
    template_name = 'accounts/login.html'
    

def logoutUser(request):
    logout(request)
    return redirect("login")
    

def homePage(request):
    return render(request, "accounts/home.html", {"hello": "hello"})


@member_allowed()
def accountMemberPage(request):
    return render(request, "accounts/userMainPage.html", {"hello": "hello"})


class AccountCompanyPage(CompanyRequiredMixin, LoginRequiredMixin, ListView):
    model = Member
    context_object_name = 'data'
    template_name = "accounts/companyMainPage.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = Member.objects.filter(company_id=self.request.user.id)
        return context

@company_allowed()
def accountCompanyPage(request):
    data = Member.objects.filter(company_id=request.user.id)
    return render(request, "accounts/companyMainPage.html", {"data": data})


@company_allowed()
def companySetTime(request):
    error = ''
    company = Company.objects.get(company_id=request.user.id)
    if request.method == 'POST':
        company.start_time = request.POST.get("start_time")
        company.end_time = request.POST.get("end_time")
        company.save()

        return HttpResponseRedirect("accounts/profile/company")
    else:
        return render(request, "accounts/companySetTime.html", {"error": error, "company": company})


@company_allowed()
def companySeeUserStat(request, user):
    member = Member.objects.get(member__username=user)
    data = WorkTime.objects.filter(member_id=member)
    return render(request, "accounts/userStat.html", {"data": data})


def redirectBasedOnUsers(request):
    if request.user.is_company == True:
        return redirect("/accounts/company")
    if request.user.is_member == True:
        return redirect("/accounts/member")

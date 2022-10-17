from ast import Return
from operator import imod
from django.shortcuts import render
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.views.generic import CreateView, ListView, View
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.core.paginator import Paginator, EmptyPage

from .forms import MemberCreationForm, LoginUserForm, CompanyCreationForm
from .models import Company, CustomUser, WorkTime, Member
from .permissions import CompanyRequiredMixin, company_allowed, MemberRequiredMixin, member_allowed, member_or_company_allowed
from .services import change_user, company_set_time, see_user_stats, create_work_time


from calendar import month
from urllib import request
from datetime import datetime



class MemberSignUpForm(CompanyRequiredMixin , CreateView):
    model = CustomUser
    form_class = MemberCreationForm
    template_name = "accounts/sign-up-members.html"
    success_url = reverse_lazy('CompanyProfilePage', kwargs={'page': 1})

    def get_form_kwargs(self):
        kwargs = super(MemberSignUpForm, self).get_form_kwargs()
        kwargs['company'] = self.request.user.company
        return kwargs


class CompanySignUpForm(CreateView):
    model = CustomUser
    form_class = CompanyCreationForm
    template_name = "accounts/sign-up-companies.html"
    success_url = reverse_lazy("login")


class LoginUser(LoginView):
    form = LoginUserForm
    template_name = 'accounts/login.html'
    

def redirectBasedOnUsers(request):
    if request.user.is_company == True:
        return redirect("/accounts/company/1")
    if request.user.is_member == True:
        return redirect("/accounts/member")


def logoutUser(request):
    logout(request)
    return redirect("login")
    

def homePage(request):
    return render(request, "accounts/home.html", {})


@member_allowed()
def accountMemberPage(request):
    member = Member.objects.get(member=request.user.id)
    
    return render(request, "accounts/userMainPage.html", {"member": member})


class AccountCompanyPage(CompanyRequiredMixin, LoginRequiredMixin, ListView):
    model = Member
    context_object_name = 'data'
    template_name = "accounts/companyMainPage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = Member.objects.filter(company_id=self.request.user.id)
        return context


@company_allowed()
def searchUsers(request):
    if request.method == "POST":
        searched = request.POST.get("searched")
        company = Company.objects.get(company=request.user)
        data = Member.objects.filter(description__contains=searched, company_id=company)

        return render(request, "accounts/searchUsers.html", {"searched": searched, "data": data})
    else:
        return render(request, "accounts/searchUsers.html", {})


@company_allowed()
def accountCompanyPage(request, page=1):
    data = Member.objects.filter(company_id=request.user.id)
    paginator = Paginator(data, 6)
    try:
        data = paginator.page(page)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
    return render(request, "accounts/companyMainPage.html", {"data": data})


@company_allowed()
def companySetTime(request):
    error = ''
    company = Company.objects.get(company_id=request.user.id)
    if request.method == 'POST':
        company_set_time(company, request)
        return redirect("/accounts/company/1")
    else:
        return render(request, "accounts/companySetTime.html", {"error": error, "company": company})


@company_allowed()
def deleteUser(request, id):
    try:
        user = CustomUser.objects.get(id=id)
        user.delete()
        return redirect("/accounts/company/1")
    except CustomUser.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")


@company_allowed()
def changeUser(request, id):
    try:
        user = CustomUser.objects.get(id=id)

        if request.method == 'POST':
            change_user(user, request)
            return redirect("/accounts/company/1")
        else:
            return render(request, "accounts/userChange.html", {"task": user})
    
    except CustomUser.DoesNotExist:
        return HttpResponseNotFound("<h2>User not found</h2>")


@member_allowed()
def createWorkTime(request):
    member = Member.objects.get(member=request.user.id)
    create_work_time(member, request)
    return render(request, "accounts/workTimeCreate.html", {"member": member, "company": member.company_id})


@member_or_company_allowed()
def seeUserStats(request, user, page=1):
    member = Member.objects.get(member__username=user)
    context = see_user_stats(member, request, page)
    return render(request, "accounts/userStat.html", context)


def totalStats(request):
    members = Member.objects.filter(company_id=request.user.id).order_by("-totalWorkTime")
    if request.method == "POST":
        members = members[::-1]
        return render(request, "accounts/totalStatistic.html", {"members": members})

    return render(request, "accounts/totalStatistic.html", {"members": members})
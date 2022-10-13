from django.shortcuts import render
from urllib import request
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.views.generic import CreateView, ListView, View
from django.contrib.auth.views import LoginView

from .forms import MemberCreationForm, LoginUserForm, CompanyCreationForm
from .models import Company, CustomUser, WorkTime, Member
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from .permissions import *
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage


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
    return render(request, "accounts/home.html", {"hello": "hello"})


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
        # data = Member.objects.filter(description__contains="firstname")
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
        company.start_time = request.POST.get("start_time")
        company.end_time = request.POST.get("end_time")
        company.secret_key = request.POST.get("secret_key")
        company.save()

        return redirect("/accounts/company/1")
    else:
        return render(request, "accounts/companySetTime.html", {"error": error, "company": company})


@company_allowed()
def companySeeUserStat(request, user, page=1):
    member = Member.objects.get(member__username=user)
    data = WorkTime.objects.filter(member_id=member)
    data = data[::-1]
    paginator = Paginator(data, 5)
    
    try:
        data = paginator.page(page)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
    totalTime = 0
    
    ontime = 0
    late = 0
    for each in WorkTime.objects.filter(member_id=member):
        if each.on_time:
            ontime += 1
        else:
            late += 1
        try:
            totalTime += each.worked
        except:
            pass
    return render(request, "accounts/userStat.html", {"data": data, "totalTime": round(totalTime, 2), "user": user, "ontime": ontime, "late": late})


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
            user.username = request.POST.get('username')
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.save()
            member = Member.objects.get(member=user)
            member.description = request.POST.get('username') + request.POST.get('first_name') + request.POST.get('last_name') + user.email
            member.save()
            return redirect("/accounts/company/1")
        else:
            return render(request, "accounts/userChange.html", {"task": user})
    
    except CustomUser.DoesNotExist:
        return HttpResponseNotFound("<h2>User not found</h2>")


@member_allowed()
def createWorkTime(request):
    member = Member.objects.get(member=request.user.id)
    try:
        workTime = WorkTime.objects.get(flag=False, member_id=member)
    except:
        workTime = False
    if request.method == "POST":
        if workTime:
            workTime.end_time = datetime.now().strftime("%H:%M")
            workTime.flag = True
            workTime.save()
            action = WorkTime.objects.get(worked=None, flag=True, member_id=member)
            action.worked = abs(round(((action.end_time.hour*60 + action.end_time.minute) - (action.start_time.hour*60 + action.start_time.minute)) / 60, 2))
            action.save()
            return redirect("/accounts/member")
        else:
            workTime = WorkTime()
            workTime.company_id = member.company_id
            workTime.member_id = request.user.member
            workTime.start_time = datetime.now().strftime("%H:%M")
            workTime.save()
            action = WorkTime.objects.get(flag=False, member_id=member)
            company = action.company_id
            if action.start_time > company.start_time:
                action.on_time = False
            else:
                action.on_time = True
            action.save()
            return redirect("/accounts/member")
    return render(request, "accounts/workTimeCreate.html", {"member": member, "company": member.company_id})


@member_allowed()
def seeUserStats(request, page=1):
    member = Member.objects.get(member=request.user)
    data = WorkTime.objects.filter(member_id=member)
    data = data[::-1]
    paginator = Paginator(data, 5)
    try:
        data = paginator.page(page)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
    totalTime = 0
    ontime = 0
    late = 0
    for each in WorkTime.objects.filter(member_id=member):
        if each.on_time:
            ontime += 1
        else:
            late += 1
        try:
            totalTime += each.worked
        except:
            pass
    
    return render(request, "accounts/userStat.html", {"data": data, "totalTime": round(totalTime, 2), "member": member, "ontime": ontime, "late": late})

from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import redirect

from .models import Member, WorkTime

from datetime import datetime

def change_user(user, request):
    user.username = request.POST.get('username')
    user.first_name = request.POST.get('first_name')
    user.last_name = request.POST.get('last_name')
    user.save()
    member = Member.objects.get(member=user)
    member.description = request.POST.get('username') + request.POST.get('first_name') + request.POST.get('last_name') + user.email
    member.save()


def company_set_time(company, request):
    company.start_time = request.POST.get("start_time")
    company.end_time = request.POST.get("end_time")
    company.secret_key = request.POST.get("secret_key")
    company.save()


def see_user_stats(member, request, page):
    dt = datetime.today().month
    data = WorkTime.objects.filter(member_id=member, created_at__month=dt)
    context = {
        "totalTime": 0,
        "ontime": 0,
        "late": 0,
        "member": member
    }
    for each in data:
        if each.on_time:
            context["ontime"] += 1
        else:
            context["late"] += 1
        try:
            context["totalTime"] += each.worked
        except:
            pass
    data = data[::-1]
    paginator = Paginator(data, 5)
    try:
        data = paginator.page(page)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
    context["data"] = data
    context['member'] = member
    return context


def create_work_time(member, request):
    try:
        workTime = WorkTime.objects.get(flag=False, member_id=member)
    except:
        workTime = False
    if request.method == "POST":
        if workTime:
            work_time_exist(workTime, member, request)
        else:
            work_time_not_exist(member, request)


def work_time_not_exist(member, request):
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


def work_time_exist(workTime, member, request):
    workTime.end_time = datetime.now().strftime("%H:%M")
    workTime.flag = True
    workTime.save()
    action = WorkTime.objects.get(worked=None, flag=True, member_id=member)
    action.worked = abs(round(((action.end_time.hour*60 + action.end_time.minute) - (action.start_time.hour*60 + action.start_time.minute)) / 60, 2))
    action.save()
    return redirect("/accounts/member")

from django.urls import path
from .views import *

urlpatterns = [
    path("members/sign-up", MemberSignUpForm.as_view(), name="mem_signup"),
    path("companys/sign-up", CompanySignUpForm.as_view(), name="comp_signup"),
    path("login", LoginUser.as_view(), name="login"),
    path("logout", logoutUser, name="logout"),

    path("", homePage, name="homePage"),
    path("accounts/", redirectBasedOnUsers, name='UserProfileRedirectPage'),
    path("accounts/member", accountMemberPage, name='UserProfilePage'),

    path("accounts/company", accountCompanyPage, name='CompanyProfilePage'),
    path("accounts/company/change", companySetTime, name='setTime'),
    path("accounts/company/<int:id>", companySeeUserStat, name='userWorktime'),
    path("accounts/company/delete/<int:id>", deleteUser, name='deleteUser'),
    path("accounts/company/change/<int:id>", changeUser, name='changeUser'),

    path("accounts/member/create", createWorkTime, name="createWorkTime"),
    path("accounts/member/stats", seeUserStats, name="seeUserStats"),
]
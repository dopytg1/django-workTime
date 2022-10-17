from django.urls import path
from .views import MemberSignUpForm, CompanySignUpForm, LoginUser, redirectBasedOnUsers, logoutUser, homePage, accountMemberPage, AccountCompanyPage, searchUsers, accountCompanyPage, companySetTime, deleteUser, changeUser, createWorkTime, seeUserStats

urlpatterns = [
    path("members/sign-up", MemberSignUpForm.as_view(), name="mem_signup"),
    path("companys/sign-up", CompanySignUpForm.as_view(), name="comp_signup"),
    path("login", LoginUser.as_view(), name="login"),
    path("logout", logoutUser, name="logout"),

    path("", homePage, name="homePage"),
    path("accounts/", redirectBasedOnUsers, name='UserProfileRedirectPage'),

    path("accounts/company/<int:page>", accountCompanyPage, name='CompanyProfilePage'),
    path("accounts/company/searchUsers/", searchUsers, name='searchUsers'),
    path("accounts/company/change", companySetTime, name='setTime'),
    path("accounts/company/<str:user>/<int:page>/", seeUserStats, name='userWorktime'),
    path("accounts/company/delete/<int:id>", deleteUser, name='deleteUser'),
    path("accounts/company/change/<int:id>", changeUser, name='changeUser'),

    path("accounts/member", accountMemberPage, name='UserProfilePage'),
    path("accounts/member/create", createWorkTime, name="createWorkTime"),
    path("accounts/member/<str:user>/<int:page>/", seeUserStats, name="seeUserStats"),
]
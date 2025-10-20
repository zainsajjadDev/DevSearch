from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.loginPage, name="login"),
    path("register/", views.registerUser, name="register"),
    path("logout/", views.logoutUser, name="logout"),
    path("", views.profiles, name="profiles"),
    path("profile/<uuid:pk>/", views.userProfile, name="user-profile"),
    path("account/", views.account, name="accounts"),
    path("edit-account/", views.editAccount, name="editAccount"),
    path("addskill", views.addSkillS, name="addSkills"),
    path("edit-skill/<uuid:pk>/", views.editSkill, name="editSkill"),
    path("delete-skill/<uuid:pk>/", views.deleteSkill, name="deleteSkill"),
    path("inbox/",views.inbox,name="inbox"),
    path("message/<uuid:pk>/" ,views.viewMessage , name = "message"),
    path("create-message/<uuid:pk>/" ,views.createMessage , name= 'create-message')

]

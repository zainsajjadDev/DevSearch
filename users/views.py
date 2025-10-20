from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile, Skill, Message
from .forms import ProfileForm, SkillForm, MessageForm
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from .validators import NameVaidator
from .utils import searchProfile, paginatorProfiles

# Create your views here.


def loginPage(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect("profiles")

    if request.method == "POST":
        username = request.POST["username"].lower()
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(
                request.GET["next"] if "next" in request.GET else "accounts"
            )
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "users/login_register.html")


def registerUser(request):
    page = "register"
    if request.user.is_authenticated:
        return redirect("accounts")

    if request.method == "POST":
        username = request.POST["username"].lower()
        email = request.POST["email"]
        password = request.POST["password"]
        password1 = request.POST["confirm-password"]

        validators = NameVaidator()
        try:
            print("validating the password")
            validators.validate(username)
        except ValidationError as e:
            for error in e:
                messages.error(request, error)
            return render(request, "users/login_register.html", {"page": page})

        # Check password match

        if password != password1:
            messages.error(request, "Passwords do not match")
            return render(request, "users/login_register.html", {"page": page})

        # Check existing user
        if User.objects.filter(username=username).exists():
            messages.error(request, "User already exists")
            return render(request, "users/login_register.html", {"page": page})

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return render(request, "users/login_register.html", {"page": page})

        # Validate password using Django validators

        try:
            validate_password(password)

        except ValidationError as e:
            for error in e:
                messages.error(request, error)
            return render(request, "users/login_register.html", {"page": page})

        # Create user
        user = User.objects.create_user(
            username=username, password=password, email=email
        )
        user.save()

        messages.success(request, "Account created successfully. Please log in.")
        return redirect("login")

    return render(request, "users/login_register.html", {"page": page})


def logoutUser(request):
    logout(request)
    messages.success(request, "User logout success")
    return redirect("login")


def profiles(request):

    profiles, search_query = searchProfile(request)
    customrange, profiles = paginatorProfiles(request, profiles, 6)
    context = {
        "profiles": profiles,
        "search_query": search_query,
        "customrange": customrange,
    }
    return render(request, "users/profiles.html", context)


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    topSkill = profile.skill_set.exclude(description__exact="")
    otherSkill = profile.skill_set.filter(description="")
    context = {
        "profile": profile,
        "otherSkill": otherSkill,
        "topSkill": topSkill,
    }
    return render(request, "users/user-profile.html", context)


@login_required(login_url="login")
def account(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    project = profile.project_set.all()
    context = {"profile": profile, "skills": skills, "projects": project}
    return render(request, "users/accounts.html", context)


@login_required(login_url="login")
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("accounts")
    context = {"form": form}
    return render(request, "users/profile_form.html", context)


@login_required(login_url="login")
def addSkillS(request):
    profile = request.user.profile
    form = SkillForm()
    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()

            return redirect("accounts")

    context = {"form": form}
    return render(request, "users/skill.html", context)


@login_required(login_url="login")
def editSkill(request, pk):
    profile = request.user.profile
    skill = Skill.objects.get(id=pk, owner=request.user.profile)

    form = SkillForm(instance=skill)
    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()

            return redirect("accounts")

    context = {"form": form}
    return render(request, "users/skill.html", context)


@login_required(login_url="login")
def deleteSkill(request, pk):
    skill = Skill.objects.get(id=pk, owner=request.user.profile)

    if request.method == "POST":
        skill.delete()
        return redirect("accounts")

    return render(request, "project/delete-project.html", {"object": skill})


@login_required(login_url="login")
def inbox(request):
    profile = request.user.profile
    messagesRequest = profile.messages.all()
    unreadCount = messagesRequest.filter(is_read=False).count
    context = {"messagesRequest": messagesRequest, "unreadCount": unreadCount}
    return render(request, "users/inbox.html", context)


@login_required(login_url="login")
def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {"message": message}
    return render(request, "users/message.html", context)


def createMessage(request, pk):
    receipient = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == "POST":
        form = MessageForm(request.POST)

        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.receipient = receipient

            if sender:
                message.name = sender.name
                message.email = sender.email

            message.save()
            messages.success(request, "message sent successfully")
            return redirect("user-profile", pk=receipient.id)
    context = {"form": form, "receipient": receipient}
    return render(request, "users/messages_form.html", context)

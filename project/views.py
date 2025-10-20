from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProjectForm, ReviewForm
from .models import Project, Review, Tag
from .utils import searchProject, paginateProjects
from django.contrib import messages

# Create your views here.


def projects(request):
    projects, search_query = searchProject(request)
    customrange, projects = paginateProjects(request, projects, 6)

    context = {
        "projects": projects,
        "customrange": customrange,
        "search_query": search_query,
    }
    return render(request, "project/projects.html", context)


def project(request, pk):
    project = Project.objects.get(id=pk)
    tags = project.tags.all()
    reviews = project.review_set.all()
    form = ReviewForm()

    if request.method == "POST":
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.project = project
            review.owner = request.user.profile
            review.save()
            project.getVoteCount
            messages.success(request, "Your comment added successfully")
            return redirect("project", pk=project.id)

    context = {"project": project, "tags": tags, "reviews": reviews, "form": form}
    return render(request, "project/project.html", context)


@login_required(login_url="login")
def createProject(request):
    form = ProjectForm()
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)

        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user.profile
            project.save()

            messages.success(request, "Project created successfully!")
            return redirect("accounts")

    context = {"form": form}
    return render(request, "project/create-project.html", context)


@login_required(login_url="login")
def updateProject(request, pk):
    project = Project.objects.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == "POST":

        form = ProjectForm(request.POST, request.FILES, instance=project)

        if form.is_valid():
            project = form.save()

            messages.success(request, "Project updated successfully!")
            return redirect("accounts")

    context = {"form": form, "project": project}
    return render(request, "project/create-project.html", context)


@login_required(login_url="login")
def deleteProject(request, pk):
    project = Project.objects.get(id=pk)
    if request.method == "POST":
        project.delete()
        return redirect("accounts")
    context = {
        "object": project,
    }
    return render(request, "project/delete-project.html", context)

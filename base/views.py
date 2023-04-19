from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm
from django.contrib.auth.decorators import login_required
from .utils import searchProject, paginateProjects
from django.contrib import messages

# Create your views here.le


def projects(request):

    projects, search_query = searchProject(request)

    custom_range, projects = paginateProjects(request,projects,6)

    context = {'projects': projects, 'search_query': search_query,'custom_range':custom_range}
    return render(request, 'base/project.html', context)

def project(request, id):
    projectObj = Project.objects.get(id=id)
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectObj
        review.owner = request.user.profile
        review.save()

        projectObj.getVoteCount

        messages.success(request,'your review is added successfully')
        return redirect('project', id=projectObj.id)

    context ={'project': projectObj, 'form':form }
    return render(request, 'base/single-project.html', context)

@login_required(login_url="login")
def createProject(request):

    profile = request.user.profile
    form = ProjectForm

    if request.method=="POST":
        newtags = request.POST.get('newtags').replace(',', " " ).split()
        form = ProjectForm(request.POST,request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag) 
            return redirect('account')

    context ={'forms': form}
    return render(request, 'base/project-form.html', context)

@login_required(login_url="login")
def updateProject(request, id):

    profile = request.user.profile
    project = profile.project_set.get(id=id)
    form = ProjectForm(instance=project)

    if request.method=="POST":
        newtags = request.POST.get('newtags').replace(',', " " ).split()
        form = ProjectForm(request.POST,request.FILES,instance=project)
        if form.is_valid():
            project = form.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
                
            return redirect('account')

    context = {'forms': form}
    return render(request, 'base/project-form.html', context)

@login_required(login_url="login")
def deleteProject(request, id):
    profile = request.user.profile
    project =  profile.project_set.get(id=id)

    if request.method=="POST":
        project.delete()
        return redirect('account')

    context = {'obj': project}
    return render(request, 'delete.html', context)


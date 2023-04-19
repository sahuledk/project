from django.shortcuts import render, redirect
from .models import Profile
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import customUserCreationForm, profileForm, skillForm, messageForm
from django.db.models import Q
from .utils import profileSearch, paginateProfiles

# Create your views here.
def profiles(request):

    profiles, search_query = profileSearch(request)
    custom_range, profiles = paginateProfiles(request,profiles,1)

    context = {'profiles': profiles, 'search_query': search_query,'custom_range': custom_range}
    return render(request,'users/profile.html', context)

def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    topSkills = profile.skills_set.exclude(description="")
    otherSkills = profile.skills_set.filter(description="")

    context = {'profile': profile,'topSkills':topSkills,'otherSkills':otherSkills}
    return render(request, 'users/user-profile.html', context)

def loginUser(request):

    if request.user.is_authenticated:
        return redirect('profiles')
    if request.method == 'POST' :
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,"Use doesn't exist")
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if next in request.GET else 'account')

        else:
            messages.error(request,"Username or Password is incorrect")

    return render(request, 'users/register-login.html')

def logoutUser(request):
        logout(request)
        messages.success(request,"User logged out Successfully")
        return redirect('login')
def registerUser(request):
    page = 'register'
    form = customUserCreationForm()
    if request.method=='POST':
        form = customUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request,'User account created Successfully')
            login(request,user)
            return redirect('edit-profile')
        else:
            messages.error(request,"An error occurred during Registration ")


    context ={'page': page,'form':form}
    return render(request,'users/register-login.html', context)

@login_required(login_url="login")
def userAccount(request):

    profile = request.user.profile
    context = {'profile': profile}
    return render(request,'users/account.html', context)

@login_required(login_url="login")
def editProfile(request):
    profile = request.user.profile
    form = profileForm(instance=profile)

    if request.method=="POST":
        form = profileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid:
            form.save()
            return redirect('account')
    context = {'form': form}
    return render(request, 'users/profile-form.html', context)

@login_required(login_url="login")
def createSkill(request):
    profile = request.user.profile
    form = skillForm()

    if request.method == 'POST':
        form = skillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request,'New skill added Successfully')
            return redirect('account')

    context = {'form': form}
    return render(request,'users/skillForm.html', context)


@login_required(login_url="login")
def updateSkill(request,pk):
    profile = request.user.profile
    skill = profile.skills_set.get(id=pk)
    form = skillForm(instance=skill)

    if request.method == 'POST':
        form = skillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request,'Skill updated created Successfully')
            return redirect('account')

    context = {'form': form}
    return render(request,'users/skillForm.html', context)
    
@login_required(login_url="login")
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skills_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request,'Skill deleted  Successfully')
        return redirect('account')

    context = {'obj': skill}
    return render(request,'delete.html', context)

@login_required(login_url="login")
def inbox(request):

    profile = request.user.profile
    messageRequests = profile.messages.all()
    unread_count = messageRequests.filter(is_read=False).count()
    context = {'messageRequests': messageRequests, 'unread_count': unread_count }
    return render(request, 'users/inbox.html', context)

@login_required(login_url="login")

def viewMessage(request, pk):

    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()

    context = {'message': message}

    return render(request, 'users/message.html' , context)

def sendMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = messageForm()

    try:
        sender = request.user.profile
    except:
        sender = None
    
    if request.method == 'POST':
        form = messageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()
            messages.success(request,'Message send')
            return redirect('user-profile', pk=recipient.id)
    context = {'recipient': recipient, 'form': form}
    return render(request, 'users/messageForm.html', context)
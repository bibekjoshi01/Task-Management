from re import I
from django.http import HttpResponse
from django.shortcuts import render, redirect
from . forms import *
from . models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Count
from django.db.models import Q
from django.contrib.auth.decorators import login_required


# Create your views here.
def register_page(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else: 
            messages.error(request, 'An unknown error occured! Try Again')
    
    context = {'form':form}
    return render(request, 'base/register.html', context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None: 
            login(request, user)
            return redirect('/')
        
        else: 
            messages.info(request, 'Email or Password is incorrect')
    
    return render(request, 'base/login.html')

def logoutuser(request):
    logout(request)
    return redirect('home')

@login_required(login_url= 'login')
def userprofile(request, pk):
    user = User.objects.get(username=pk)

     #groups = user.room_set.all()
    groups = Room.objects.filter(admin=user)
    
    all_groups = Room.objects.filter(members=user)
    return render(request, 'base/profile.html', {'user':user, 'groups':groups, 'all_groups':all_groups})

@login_required(login_url= 'login')
def edituserprofile(request):
    user = request.user
    form = userForm(instance=user)
    
    if request.method == 'POST':
        form = userForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=user.username)
    return render(request, 'base/edit-profile.html', {'form': form})

@login_required(login_url= 'login')
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    groups = Room.objects.filter(Q(topic__name__icontains=q)|
                                Q(name__icontains=q) |
                                Q(description__icontains=q)
                                )[:5]

    top_groups = Room.objects.alias(
        num_members = Count('members')
    ).order_by('-num_members')[:5]

    group_count = groups.count()
    

    topics = Topic.objects.all()

    context = {'q':q, 'groups':groups, 'group_count':group_count, 'topics':topics, 'top_groups':top_groups}
    return render(request, 'base/home.html', context)


@login_required(login_url= 'login')
def create_group(request):
    form = GroupForm()

    if request.method == 'POST':
        form = GroupForm(request.POST, request.FILES)
        if form.is_valid():
            form.admin = request.user
            form.topic = request.POST.get('topic').title()
            form.save()
            return redirect('home')
        else:
            form = GroupForm()

    context = {'form':form}
    return render(request, 'base/create_room.html', context)

@login_required(login_url= 'login')
def group(request, pk):
    group = Room.objects.get(id=pk)
    members = group.members.all()

    context = {'group':group, 'members':members}
    return render(request, 'base/group.html', context)


def join_group(request,pk):
    group = Room.objects.get(id=pk)
    group.members.add(request.user)
    return redirect('group', pk=pk)


def leave_group(request,pk):
    group = Room.objects.get(id=pk)
    group.members.remove(request.user)
    return redirect('group', pk=pk)

@login_required(login_url= 'login')
def edit_group(request, pk):
    group = Room.objects.get(id=pk)
    topics = Topic.objects.all()
    form = GroupForm(instance=group)

    if request.user != group.admin: 
        return redirect('home')

    if request.method == 'POST':
        form = GroupForm(request.POST, request.FILES, instance=group)
        if form.is_valid():
            topic_name = request.POST.get('topic')
            topic, created = Topic.objects.get_or_create(name=topic_name)
            group.topic = topic
            form.save()
            return redirect('group', pk=pk)


    context = {'form':form, 'topics': topics, 'group':group}
    return render(request, 'base/edit-group.html', context)

def delete_group(request, pk):
    group = Room.objects.get(id=pk)

    if request.user != group.admin: 
        return redirect('home')

    if request.method == 'POST':
        group.delete()
        return redirect('home')
    obj = group.name

    context = {'group':group, 'obj':obj}
    return render(request, 'base/delete.html', context)

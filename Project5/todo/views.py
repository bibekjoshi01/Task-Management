from django.shortcuts import render, redirect
from . models import *
from . forms import TaskForm
# Create your views here.

def home(request):
    tasks = Task.objects.all()
    complete = Task.objects.filter(complete=True).count()
    incomplete = Task.objects.filter(complete=False).count()
    context={'tasks':tasks, 'complete':complete, 'incomplete':incomplete}
    return render(request, 'home.html', context)


# def task_detail(request,pk):
#     tasks = Task.objects.get(id=pk)
#     return render(request, 'task.html', {'tasks':tasks})


def create_task(request):
    form = TaskForm()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/')

    return render(request, 'create_task.html', {'form':form})


def update_task(request, pk):
    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
        return redirect('/')

    return render(request, 'create_task.html', {'form':form})

def delete_task(request, pk):
    task = Task.objects.get(id=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('/')
    
    return render(request, 'delete_task.html')
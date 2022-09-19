from . models import *
from django.forms import ModelForm


class TaskForm(ModelForm):
    tasks = Task.objects.all()

    class Meta: 
        model = Task
        fields = '__all__'
        exclude = ['user']
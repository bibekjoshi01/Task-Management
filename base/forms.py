from django import forms 
from django.contrib.auth.forms import UserCreationForm
from . models import *
from django.forms import ModelForm

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

class GroupForm(ModelForm):
    class Meta:
        model = Room
        widgets = {
            'description': forms.Textarea(
                attrs = {'placeholder':'Write something about your group ....'}
            ),
            'name': forms.TextInput(
                attrs = {'placeholder':'Programming Hub'}
        )
        }
        fields = ['name', 'description', 'group_photo']

class userForm(ModelForm):
    class Meta:
        model = User
        fields = ['profile_pic', 'first_name', 'last_name', 'email', 'bio']
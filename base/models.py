from re import M
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    bio = models.TextField(max_length=100, null=True, blank=True)
    profile_pic = models.ImageField(null=True, default='avatar.svg')
    #details model remaining 
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Topic(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Room(models.Model):
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    group_photo = models.ImageField(null=True, upload_to = 'images/', default='avatar.svg')
    name = models.CharField(unique=True, max_length=100)
    description = models.TextField(null=True, blank=True)
    members = models.ManyToManyField(User, related_name='members', blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta: 
        ordering = ['-created']
    
    def __str__(self):
        return self.name

# message functionality remaining. 
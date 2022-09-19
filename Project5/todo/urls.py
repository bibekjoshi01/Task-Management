from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    #path('task_detail/<str:pk>', views.task_detail, name='task_detail'),
    path('create_task', views.create_task, name="create_task"),
    path('update_task/<str:pk>', views.update_task, name="update_task"),
    path('delete_task/<str:pk>', views.delete_task, name="delete_task"),


]

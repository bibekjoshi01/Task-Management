from unicodedata import name
from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home, name="home"),
    path('logout', views.logoutuser, name="logout"),
    path('login', views.login_page, name="login"),
    path('register', views.register_page, name="register"),
    path('profile/<str:pk>', views.userprofile, name="profile"),
    path('edit-profile', views.edituserprofile, name="edit-profile"),


    path('create_group', views.create_group, name="create-group"),
    path('edit-group/<str:pk>', views.edit_group, name="edit-group"),
    path('delete-group/<str:pk>', views.delete_group, name="delete-group"),
    path('group/<str:pk>', views.group, name="group"),
    path('join_group/<str:pk>', views.join_group, name="join_group"),
    path('leave_group/<str:pk>', views.leave_group, name="leave_group"),




]

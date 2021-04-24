from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('login',views.user_login,name="user_login"),
    path('signup',views.user_signup,name="user_signup"),
    path('add_todo',views.add_todo,name="add_todo"),
    path('logout',views.user_logout,name='user_logout'),
    path('delete_todo/<int:id>',views.delete_todo,name="delete_todo"),
    path('change_status/<int:id>/<str:status>',views.change_status,name="change_status"),
    path('emailme',views.emailme,name="emailme"),
    path('profile',views.profile,name='profile')
]

from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    # path('blogpost', views.blogpost, name='blogpost'),
    path('welcome', views.welcome, name='welcome'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    # path('begin', views.begin, name='begin'),
    path('next_clue', views.next_clue, name='next_clue'),
    path('completion', views.completion, name='completion'),
]
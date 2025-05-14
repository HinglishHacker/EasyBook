from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views
from .views import login_view, register_view, logout_then_login

urlpatterns = [
    path('register/', register_view, name='register'),
    path('logout/', logout_then_login, name='logout'),
    path('login/', views.login_view, name='login'),
    path('', views.home_view, name='base'),
]

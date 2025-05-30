from django.urls import path
from .views import home_view, about_view
from . import views

app_name = 'main'

urlpatterns = [
    path("", home_view, name="home"),
    path('about/', views.about_view, name='about'),
]


from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views
from views import login_view
# router = DefaultRouter()
# router.register(r'passengers', views.PassengerViewSet)

# urlpatterns = router.urls + 
urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('', views.home_view, name='base'),
    path('login/', login_view.as_view(template_name='login.html'), name='login'),
]

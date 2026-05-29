
from django.contrib import admin
from django.urls import path
from app import views
from .api import api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.render_home, name="home"),
    path('about/', views.render_about, name="about"),
    path('api/', api.urls),
    path('api-playground/', views.api_playground, name="api_playground"),
]
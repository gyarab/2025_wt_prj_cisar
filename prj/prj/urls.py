
from django.contrib import admin
from django.urls import path
from app import views
from ninja import NinjaAPI
from .api import api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.render_home, name="home"),
    path('about/', views.render_about, name="about"),
    path('api/', api.urls),
]

from . import api

api = NinjaAPI()

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),  
]

urlpatterns = [
    path("api-playground/", views.api_playground, name="api_playground"),
]

from django.contrib import admin
from django.urls import path
from app import views
from ninja import NinjaAPI

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.render_home, name="home"),
    path('about/', views.render_about, name="about"),
]

from prj.api import api

api = NinjaAPI()

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),  
]
from django.contrib import admin
from .models import Team, Player

admin.site.register(Team)
admin.site.register(Player)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'stadium', 'colours')
    

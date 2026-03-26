from django.contrib import admin
from .models import Team, Player, Match, Statistics


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'stadium', 'colours', 'founded_year')

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'position', 'number', 'team')

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('home_team', 'away_team', 'date', 'stadium', 'score_home', 'score_away')

@admin.register(Statistics)
class StatisticsAdmin(admin.StatisticsAdmin):
    list_display = ('goals', 'assist', 'penalty_minutes')


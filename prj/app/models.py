from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=100)
    stadium = models.CharField(max_length=100)
    colours = models.CharField(max_length=100)
    founded_year = models.IntegerField()
    

    def __str__(self):
        return self.name

class Player(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    position = models.CharField(max_length=100)
    number = models.IntegerField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Match(models.Model):
    home_team = models.ForeignKey(Team, related_name='home_matches', on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name='away_matches', on_delete=models.CASCADE)
    score_home = models.IntegerField(default=0)
    score_away = models.IntegerField(default=0)
    date = models.DateTimeField()
    stadium = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.home_team.name} vs {self.away_team.name} on {self.date}"

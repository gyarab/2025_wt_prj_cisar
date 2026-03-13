from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=100)
    stadium = models.CharField(max_length=100)
    colours = models.CharField(max_length=100)
    

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
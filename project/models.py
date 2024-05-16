import datetime

from django.db import models

from app.models import Team, Tournament, Player
# Create your models here.

class PlayerStat(models.Model):
    date = models.DateField()
    player = models.ForeignKey(Player, default=None, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.player.first_name

class GoalStat(models.Model):
    tournament = models.ForeignKey(Tournament, default=None, on_delete=models.SET_NULL, null=True, blank=True)
    player = models.ForeignKey(PlayerStat, default=None, on_delete=models.SET_NULL, null=True, blank=True)
    time = models.TimeField()
    goal_scored = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.player.first_name} {self.tournament.name} {self.goal_scored}'

class AssitStat(models.Model):
    tournament = models.ForeignKey(Tournament, default=None, on_delete=models.SET_NULL, null=True, blank=True)
    player = models.ForeignKey(PlayerStat, default=None, on_delete=models.SET_NULL, null=True, blank=True)
    time = models.TimeField()
    assit_made = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.player.first_name} {self.tournament.name} {self.assit_made}'

class OtherStat(models.Model):
    tournament = models.ForeignKey(Tournament, default=None, on_delete=models.SET_NULL, null=True, blank=True)
    player = models.ForeignKey(PlayerStat, default=None, on_delete=models.SET_NULL, null=True, blank=True)
    stat = models.PositiveIntegerField()
    time = models.TimeField()

    def __str__(self):
        return f'{self.player.first_name} {self.tournament.name} {self.stat}'

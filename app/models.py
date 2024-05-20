import uuid

from django.db import models
from django.utils.safestring import mark_safe

# Create your models here.


class Tournament(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name.title()

    
class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='club_logos', null=True, blank=True)
    slug = models.SlugField(default=uuid.uuid4, null=True, blank=True)
    league = models.ForeignKey(Tournament, default=None, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name.title()

    def club_logo_img(self):
        if self.logo:
            return mark_safe(
                '<img src="/media/%s" width="50" height="50" /.>' %(self.logo)
                )
        return None

    @property
    def logo_url(self):
        try:
            url = self.logo.url
        except:
            url = ''
        return url

    class Meta:
        ordering = ['name']

class Player(models.Model):
    first_name = models.CharField(max_length=500)
    last_name = models.CharField(max_length=500)
    other_name = models.CharField(max_length=500, blank=True)
    club = models.ForeignKey(Team, default=None, null=True, on_delete=models.SET_NULL)
    date_of_birth = models.DateField(blank=True)
    nationality = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.other_name}'

    def player_age(self):
        """
        today = datetime.date.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        """
        age = datetime.date.today()-self.date_of_birth
        return int((age).days/365.25)


class Season(models.Model):
    name = models.CharField(max_length=100)
    year = models.IntegerField()

    class Meta:
        ordering = ['name','year']

    def __str__(self):
        return self.name.title()


class ClubPoint(models.Model):
    GROUND = (
        ('Home', 'Home'),
        ('Away', 'Away'),
        ('Neutral', 'Neutral'),
    )

    OUTCOME = (
        ('W', 'Win'),
        ('D', 'Draw'),
        ('L', 'Lose'),
    )

    MATCHWEEK = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10),
        (11, 11),
        (12, 12),
        (13, 13),
        (14, 14),
        (15, 15),
        (16, 16),
        (17, 17),
        (18, 18),
        (19, 19),
        (20, 20),
        (21, 21),
        (22, 22),
        (23, 23),
        (24, 24),
        (25, 25),
        (26, 26),
        (27, 27),
        (28, 28),
        (29, 29),
        (30, 30),
        (31, 31),
        (32, 32),
        (33, 33),
        (34, 34),
        (35, 35),
        (36, 36),
        (37, 37),
        (38, 38),
    )

    
    season  = models.ForeignKey(Season, default=None, null=True, on_delete=models.SET_NULL)
    date = models.DateField(blank=True, null=True)
    club = models.ForeignKey(Team, default=None, null=True, on_delete=models.SET_NULL, related_name='Club')
    club_against = models.ForeignKey(Team, default=None, null=True, on_delete=models.SET_NULL, related_name='Club_against')
    tournament = models.ForeignKey(Tournament, default=None, null=True, on_delete=models.SET_NULL)
    point = models.PositiveIntegerField(blank=True, null=True)
    total_point = models.PositiveIntegerField(blank=True, null=True)
    ground = models.CharField(max_length=50, choices=GROUND)
    outcome = models.CharField(max_length=10, choices=OUTCOME)
    matchweek = models.PositiveIntegerField(blank=True, null=True, choices=MATCHWEEK)
    goals_scored = models.PositiveIntegerField(blank=True, null=True)
    goals_against = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        if self.ground == 'Away':
            return f'{self.club_against}-{self.club} {self.outcome} {self.ground}'
        return f'{self.club}-{self.club_against} {self.outcome} {self.ground}'
    
    def save(self, *args, **kwargs):
        from django.db.models import Sum, F
        from django.db.models.expressions import Window
        from django.db.models.functions import Rank
        
        if self.outcome == 'W' and self.tournament.id == 1:
            self.point = int(3)
        elif self.outcome == 'D' and self.tournament.id == 1:
            self.point = int(1)
        else:
            self.point = int(0)
        
        season_ = ClubPoint.objects.filter(season=self.season, club=self.club, matchweek__lte=self.matchweek).values('season').annotate(total=Sum('point'))
        if season_.exists():
            print('tt', season_)
            season = [f"{item['total']}" for item in season_]
            print('uu', season[0])
            print(season)
            if season == ['None']:
                self.total_point = self.point
                print(self.total_point)
            else:
                self.total_point = season[0]
                print(season[0])
        else:
            pass

        position = ClubPoint.objects.filter(season=self.season).annotate(
            rank=Window(
                expression=Rank(),
                order_by=F('point').desc()
            ),
        )
        print(position)
        
        super(ClubPoint, self).save(*args, **kwargs)

class MatchDay(models.Model):
    touranment = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_team')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_team')
    home_score = models.PositiveIntegerField()
    away_score = models.PositiveIntegerField()
    date = models.DateTimeField()

    def __str__(self):
        return f'{self.home_team.name} {self.home_score} - {self.away_team.name} {self.away_score}'


class MatchDayScorer(models.Model):
    match_day = models.ForeignKey(MatchDay, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.team.name} {self.player.first_name} {self.score}'
    




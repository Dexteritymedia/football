from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Team, Tournament, ClubPoint, Season 

User = get_user_model()


GOALS = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
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


OUTCOME = (
        (None, ''),
        ('W', 'Win'),
        ('D', 'Draw'),
        ('L', 'Lose'),
    )


GROUND = (
        (None, ''),
        ('Home', 'Home'),
        ('Away', 'Away'),
    )

GOALS_TYPE = (
        ('GF', 'Goals scored'),
        ('GA', 'Goals conceded'),
    )

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class AllClubForm(forms.Form):
    clubs = forms.ModelMultipleChoiceField(queryset=Team.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={"id":"club_id"}))
    tournament = forms.ModelMultipleChoiceField(queryset=Tournament.objects.all(), widget=forms.RadioSelect(attrs={"id":"tournament"}))
    #clubs_s = forms.ModelMultipleChoiceField(queryset=Team.objects.all(), widget=forms.SelectMultiple)
    #clubs_ss = forms.ModelMultipleChoiceField(queryset=Team.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={"class":"btn btn-success"}))
    start_date = forms.DateField()
    end_date = forms.DateField(label="End Date",widget=forms.DateInput(attrs={"class":"form-control", "type":"date", "id":"end_date"}))
    minutes = forms.IntegerField(help_text='Minutes Played', widget=forms.NumberInput(attrs={'type':'range', 'step': '5', 'min': '0', 'max': '1000', 'id':'minutes'}), required=False)
    goal = forms.ChoiceField(label="Goals", help_text='Enter a goal', choices = GOALS)
    goal_in_match = forms.ChoiceField(label="Goal scored in a match", choices = GOALS)


class ClubPointForm(forms.Form):
    
    season = forms.ModelMultipleChoiceField(queryset=Season.objects.all(), widget=forms.SelectMultiple)
    matchweek = forms.ChoiceField(label="Match Week", help_text='Enter a match week', choices=MATCHWEEK)


class MatchForm(forms.Form): 
    club = forms.ModelChoiceField(queryset=Team.objects.filter(league__name='Premier League'))
    matchweek = forms.ChoiceField(label="Match Week", required=False, help_text='Enter a match week', choices=MATCHWEEK, widget=forms.HiddenInput(),)
    outcome = forms.ChoiceField(label="Match Outcome", required=False, initial='D', choices=OUTCOME, widget=forms.HiddenInput())
    ground = forms.ChoiceField(required=False, label="Match Ground", choices=GROUND)
    tournament = forms.ModelChoiceField(required=False, queryset=Tournament.objects.all())
    opponent = forms.ModelChoiceField(required=False, queryset=Team.objects.filter(league__name='Premier League'))
    start_date = forms.DateField(label="Start Date",widget=forms.DateInput(attrs={"class":"form-control", "type":"date", "id":"start_date"}))
    end_date = forms.DateField(label="End Date",widget=forms.DateInput(attrs={"class":"form-control", "type":"date", "id":"end_date"}))


class TeamGoalForm(forms.Form): 
    club = forms.ModelChoiceField(queryset=Team.objects.filter(league__name='Premier League'))
    no_of_goals = forms.IntegerField(initial=2)
    goals = forms.ChoiceField(choices=GOALS_TYPE, widget=forms.HiddenInput())
    start_date = forms.DateField(label="Start Date", required=False, widget=forms.DateInput(attrs={"class":"form-control", "type":"date", "id":"start_date"}))
    end_date = forms.DateField(label="End Date", required=False, widget=forms.DateInput(attrs={"class":"form-control", "type":"date", "id":"end_date"}))

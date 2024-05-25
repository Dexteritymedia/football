from django.contrib import admin

from .models import (
    PlayerStat, GoalStat, AssitStat, OtherStat,
)
from app.models import Team, Tournament, Player, MatchDay, MatchDayScorer

# Register your models here.

class PlayerStatAdmin(admin.TabularInline):
    model = PlayerStat

class GoalStatAdmin(admin.TabularInline):
    model = GoalStat

class AssitStatAdmin(admin.TabularInline):
    model = AssitStat

class OtherStatAdmin(admin.TabularInline):
    model = OtherStat

class PlayerStatAdmin(admin.ModelAdmin):
   inlines = [GoalStatAdmin, AssitStatAdmin, OtherStatAdmin]


class MatchDayAdmin(admin.TabularInline):
    model = MatchDay

class MatchDayScorerAdmin(admin.TabularInline):
    model = MatchDayScorer

class MatchDayAdmin(admin.ModelAdmin):
   inlines = [MatchDayScorerAdmin,]


class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'club_logo_img', 'number_of_matches_per_team',]


class TournamentAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'number_of_team_entry', 'number_of_clubs_entry']

    
admin.site.register(PlayerStat, PlayerStatAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Tournament, TournamentAdmin)
admin.site.register(GoalStat)
admin.site.register(AssitStat)
admin.site.register(Player)
admin.site.register(MatchDay, MatchDayAdmin)
#admin.site.register(MatchDayScorer)
admin.site.register(OtherStat)

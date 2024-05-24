from django.contrib import admin

# Register your models here.

from .models import (
    ClubPoint, Season, PlayerRecord, Position, PlayerNationality, BirthYear
)

admin.site.register(ClubPoint)
admin.site.register(Season)
admin.site.register(PlayerRecord)
admin.site.register(Position)
admin.site.register(PlayerNationality)
admin.site.register(BirthYear)

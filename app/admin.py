from django.contrib import admin

# Register your models here.

from .models import (
    ClubPoint, Season
)

admin.site.register(ClubPoint)
admin.site.register(Season)

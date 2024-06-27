from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Team, ClubPoint


class TeamListSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    #protocol = 'http'

    def items(self):
     #return Team.objects.all()
     return ['team-list-page']

    def location(self, item):
        return reverse(item)


class TeamSitemap(Sitemap):

    changefreq = "daily"
    priority = 0.8

    def items(self):
        # Assuming you have a method to fetch episodes
        #return ClubPoint.objects.all()
        from django.db.models import Q
        return ClubPoint.objects.filter(Q(club__league__name='Premier League'))


class StaticSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8
    #protocol = 'https'

    def items(self):
        return ['match-search', 'team-goal-search']

    def location(self, item):
        return reverse(item)

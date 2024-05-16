from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import Http404, HttpResponse, HttpResponseForbidden, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.safestring import mark_safe
from django.core.paginator import Paginator
from django.views.generic import TemplateView, View, DetailView
from django.views.generic.edit import FormMixin
from django.urls import reverse

from .models import *
from .forms import AllClubForm, ClubPointForm, MatchForm

User = get_user_model()

# Create your views here.

def home(request):
    context = {}
    return render(request, 'app/home.html', context)

def search_page(request):
    form = AllClubForm()
    #url = reverse('')
    #url_with_params = 
    #return HttpResponseRedirect(url_with_params)
    return render(request, 'app/search_page.html', {'form': form})


class ClubDetailView(FormMixin, DetailView):
    model = Team
    slug_field = "slug"
    context_object_name = 'club'
    template_name = 'app/club_detail.html'
    pk_url_kwarg = "pk"
    slug_url_kwarg = 'slug'
    query_pk_and_slug = True
    form = MatchForm

    def get_context_data(self, **kwargs):
        context = super(ClubDetailView, self).get_context_data(**kwargs)
        #context['form'] = MatchForm(request.GET)
        return context

    """
    def get(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            try:
                club = form.cleaned_data['club']
                matchweek = form.cleaned_data['matchweek']
                outcome = form.cleaned_data['outcome']
                results = ClubPoint.objects.filter(club__name=club[0], matchweek=int(matchweek), outcome=outcome).order_by('-total_point')
                print(results)
                return render(request, 'app/match_search.html', {'form': form, 'results':results})
            except:
                
                return HttpResponse("None")

        return render(request, 'app/match_search.html', {'form': form})
    """
class SearchView(View):
    query = None
    results = []
    form_class = ClubPointForm

    def get(self, request):
        form = self.form_class(request.GET)
        if form.is_valid():
            try:
                season = form.cleaned_data['season']
                matchweek = form.cleaned_data['matchweek']
                results = ClubPoint.objects.filter(season__name=season[0], matchweek=int(matchweek)).order_by('-total_point')
                print(results)
                return render(request, 'app/search.html', {'form': form, 'results':results})
            except:
                return HttpResponse("None")

        return render(request, 'app/search.html', {'form': form})



class SearchMatchView(View):
    query = None
    results = []
    form_class = MatchForm

    def get(self, request):
        form = self.form_class(request.GET)
        if form.is_valid():
            club = form.cleaned_data.get('club', None)
            matchweek = form.cleaned_data['matchweek']
            outcome = form.cleaned_data['outcome']
            ground = form.cleaned_data.get('ground', None)
            opponent = form.cleaned_data.get('opponent', None)
            tournament = form.cleaned_data['tournament']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            print(club[0])
            print(matchweek)
            print(outcome)
            print(start_date)
            print(end_date)
            print(ground)
            print(opponent)

            if matchweek:
            
                results = ClubPoint.objects.filter(
                    club__name=club[0], date__range=(start_date, end_date), matchweek=int(matchweek),
                ).all()
                #print(results)
            elif outcome:
                results = ClubPoint.objects.filter(
                    club__name=club[0], outcome=outcome, date__range=(start_date, end_date),
                ).all()
                #print(results)
            elif tournament:
                results = ClubPoint.objects.filter(
                    club__name=club[0], date__range=(start_date, end_date),
                    tournament=tournament
                ).all()
                #print(results)
            elif opponent:
                results = ClubPoint.objects.filter(
                    club__name=club[0], date__range=(start_date, end_date), club_against=opponent
                ).all()
                #print(results)
            elif ground:
                results = ClubPoint.objects.filter(
                    club__name=club[0], ground=ground, date__range=(start_date, end_date),
                ).all()
                #print(results)
            else:
                results = ClubPoint.objects.filter(
                    club__name=club[0], date__range=(start_date, end_date),
                ).all()
                #print(results)
            return render(request, 'app/search_result.html', {'results':results})
        
        """
            except:
                
                return HttpResponse("None")
        """

        return render(request, 'app/match_search.html', {'form': form})


def searchform(request):
    if request.method == "POST":
        form = MatchForm(request.POST)
        if form.is_valid():
            club = form.cleaned_data['club']
            matchweek = form.cleaned_data['matchweek']
            outcome = form.cleaned_data['outcome']
            print(outcome)
            results = ClubPoint.objects.filter(club__name=club, matchweek=int(matchweek), outcome=outcome)
            print(results)
            return render(request, 'app/match_search_page.html', {'results': results})
    else:
        form = MatchForm()
            
    return render(request, 'app/match_search_page.html', {'form': form})

import csv
import json

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
from django.db.models import Q
from django.core import serializers
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Sum, F, Count, Func, Window, Avg, Max, Min

from .models import *
from .forms import AllClubForm, ClubPointForm, MatchForm, TeamGoalForm

User = get_user_model()

# Create your views here.

def home(request):
    context = {}
    return render(request, 'app/index.html', context)


def payment_page(request):
    context ={}
    return render(request, 'app/payment_page.html', context)


def team_list_page(request):
    #teams = Team.objects.all()
    teams = Team.objects.filter(Q(league__name='Premier League')| Q(league__name='La Liga')| Q(league__name='Bundesliga'))
    latest_season = Season.objects.last()
    context = {'teams': teams, 'season':latest_season}
    return render(request, 'app/team_list.html', context)


def team_goal_analysis_page(request, team, slug, season):
    team = Team.objects.get(name=team, slug=slug)
    #season = Season.objects.get(name=season, year=2024)
    team_data = ClubPoint.objects.filter(club__name=team, season__name=season)
    queryset = Q()
    #queryset = Q(tournament__name='Premier League')| Q(tournament__name='La Liga')
    total_goals_scored = ClubPoint.objects.filter(club__name=team, season__name=season).aggregate(gs=Sum('goals_scored'), gc=Sum('goals_against'))
    #goals_conceded= ClubPoint.objects.filter(club__name=team, season__name=season).aggregate(Sum('goals_against'))
    #ClubPoint.objects.filter(club__name=team, season=season)
    goal_diff = ClubPoint.objects.filter(club__name=team, season__name=season,).filter(queryset).annotate(gd=Sum(F('goals_scored')+F('goals_against')))
    cumulative_goals = ClubPoint.objects.filter(
        club__name=team,
        season__name=season,
        #tournament__name='Premier League',
        ).annotate(
            cumbalance=Window(Sum('goals_scored'), order_by=F('matchweek').asc())
            ).order_by('matchweek')
    """
    annotate(
        cumsum=Func(
        Sum('goals_scored'),
        template='%(expressions)s OVER (ORDER BY %(order_by)s)',
        order_by="matchweek"
        )
    ).values('matchweek', 'cumsum').order_by('matchweek', 'cumsum')
    """
    value_list = ClubPoint.objects.filter(
        club__name=team,
        season__name=season,
        tournament__name="Premier League"
        ).values_list('club_against__name', flat=True).order_by('club_against').distinct()

    print(value_list)
    group_by_value = {}
    for value in value_list:
        group_by_value[value] = team_data.filter(club_against__name=value).order_by('ground').distinct()

    #team_groupby = team_data.values('outcome').annotate(match_outcome=Count('outcome'))

    print('Team', group_by_value)

    team_value_list = team_data.values_list('outcome', flat=True).order_by('outcome').distinct()

    group_by_team_value = {}
    for value in team_value_list:
        group_by_team_value[value] = team_data.filter(outcome=value)




    context = {
        'team_data':team_data,
        'team':team,
        
        'goals_scored':total_goals_scored,
        'goal_diff':goal_diff,
        'c_goals':cumulative_goals,
        
        'group_by_value':group_by_value,
        'value_list':value_list,
        
        #'team_groupby': team_groupby,
        
        'team_value_list': team_value_list,
        'group_by_team_value': group_by_team_value,
        
        #'goals_conceded':goals_conceded
    }

    return render(request, 'app/goal_analysis.html', context)


def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data.csv"'

    writer = csv.writer(response)
    writer.writerow(['Matchweek', 'Outcome', 'Date', 'Point', 'Total point',
        'Goals against', 'Goals scored', 'Club against', 'Ground',
        'Club','Season', 'Tournament'])

    data = ClubPoint.objects.all().values_list(
        'matchweek', 'outcome', 'date', 'point', 'total_point',
        'goals_against', 'goals_scored', 'club_against__name', 'ground',
        'club__name','season__name', 'tournament__name'
    )
    for obj in data:
        writer.writerow(obj)

    return response


class TeamSearchGoalView(View):
    query = None
    results = []
    form_class = TeamGoalForm

    def get(self, request):
        form = self.form_class(request.GET)
        if form.is_valid():
            club = form.cleaned_data.get('club', None)
            no_of_goals = form.cleaned_data['no_of_goals']
            goals = form.cleaned_data['goals']
            date = form.cleaned_data['date']
            print(goals)

            print(club)
            
            query = Q()

            if date and date != "null":
                query &= Q(date__gte=date)

                

            value_list = ClubPoint.objects.filter(club=club, goals_scored=int(no_of_goals)).filter(query).values_list('outcome', flat=True).order_by('outcome').distinct()
            print('value', value_list)
            group_by_value = {}
            for value in value_list:
                group_by_value[value] = ClubPoint.objects.filter(club=club, goals_scored=int(no_of_goals), outcome=value).filter(query)

            print(group_by_value)

            return render(request, 'app/team_goals_result_page.html', {'results': group_by_value, 'club':club, 'goals':no_of_goals, 'date':date})
            
        else:
            return render(request, 'app/team_search_goal.html', {'form':form})

        return render(request, 'app/team_search_goal.html', {'form': form})


class SearchMatchView(View):
    query = None
    results = []
    form_class = MatchForm

    def get(self, request):
        form = self.form_class(request.GET)
        form.fields['outcome'].initial = None
        if form.is_valid():
            club = form.cleaned_data.get('club', None)
            matchweek = form.cleaned_data['matchweek']
            outcome = form.cleaned_data['outcome']
            ground = form.cleaned_data.get('ground', None)
            opponent = form.cleaned_data.get('opponent', None)
            tournament = form.cleaned_data['tournament']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            print(club)
            print(matchweek)
            print(outcome)
            print(start_date)
            print(end_date)
            print(ground)
            print(opponent)
            print(tournament)

            query = Q()

            query &= Q(date__range=(start_date, end_date))

            if club and club != "null":
                query &= Q(club=club)
            
            if matchweek and matchweek != "null":
                query &= Q(matchweek=matchweek)

            if outcome and outcome != "null":
                query &= Q(outcome=outcome)

            if tournament and tournament != "null":
                query &= Q(tournament=tournament)

            if opponent and opponent != "null":
                query &= Q(club_against__name=opponent)
                print('Opponent', query)

            if ground and ground != "null":
                query &= Q(ground=ground)

            print(query)

            results = ClubPoint.objects.filter(query).all()
            #print(results)
            #print(str(results.query))

            groupby = ClubPoint.objects.filter(query).values('outcome').annotate(match_outcome=Count('outcome'))
            print(groupby)

            value_list = ClubPoint.objects.filter(query).values_list('outcome', flat=True).order_by('outcome').distinct()
            print(value_list)

            group_by_value = {}
            for value in value_list:
                group_by_value[value] = ClubPoint.objects.filter(query).filter(outcome=value)

            print(type(group_by_value))

            """
            qs = (
                ClubPoint.objects.filter(query)
                .select_related("b", "c", "d")  # This is the join. You'll need to use the reverse-lookups, forward-lookups
                .values("b__name", "d__id") # This will produce a group by
                .annotate(Sum(all_data="all_data"), Sum(today_data="today_data")  # This is the aggregation part
                          .values("standard_name")  # Here put all the other fields
                          .order_by("b__type", "b__name")  # finally the order by
                          )
                )
            """

            paginator = Paginator(results, 10)

            page = request.GET.get('page')
            page_obj = paginator.get_page(page)
            try:
                posts = paginator.page(page)
            except PageNotAnInteger:
                posts = paginator.page(1)
            except EmptyPage:
                posts = paginator.page(paginator.num_pages)

            return render(request, 'app/match_result_page.html', {
                'results': group_by_value, 'page_obj': page_obj, 'club':club,
                'opponent':opponent, 'tournament':tournament, 'start_date': start_date, 'end_date':end_date,
                })
            """
            if request.user.is_authenticated:
                return render(request, 'app/match_result_page.html', {'results': results})
            else:
                request.session['results'] = serializers.serialize('json', list(results))
                return redirect('result-page')
            """
        else:
            return render(request, 'app/match_search.html', {'form':form})

        return render(request, 'app/match_search.html', {'form': form})


def result_page(request):
    if 'results' in request.session:
        context = {}
        context['results'] = request.session['results']
        print(context['results'])
        return render(request, 'app/match_result_page.html', context)
    
    return render(request, 'app/match_result_page.html')


def update_data(request):
    #update_club = ClubPoint.objects.filter(club__name='Chelsea').update(club=Team.objects.get_or_create(name='Tottenham')[0])

    #update_all = ClubPoint.objects.filter(club_against__name='Eng Arsenal').update(club_against=Team.objects.get_or_create(name='Arsenal')[0])

    return export_csv(request)

def filter_data(request):
    start_date = '2000-08-19'
    end_date = '2005-05-15'
    filter_club = ClubPoint.objects.filter(club__name='Chelsea', date__range=(start_date, end_date))
    print(filter_club.count())
    print(len(filter_club))

    season = Season.objects.all().values()
    print(season.count())

    #club_season = ClubPoint.objects.filter(club__name='Chelsea', )

    return HttpResponse("Done")


def delete_certain_data(request):
    start_date = '2000-08-19'
    end_date = '2005-05-15'
    filter_club = ClubPoint.objects.all()
    #filter_club = ClubPoint.objects.filter(club__name='Manchester City').all()
    print(filter_club.count())
    print(len(filter_club))

    #filter_club.delete()

    return HttpResponse("Done")


#####
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

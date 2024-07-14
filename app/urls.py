from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('head-to-head-search/', views.SearchMatchView.as_view(), name='match-search'),
    path('pl-teams/', views.team_list_page, name='pl-team-list-page'),
    path('<team>-goals-breakdown/<slug>/<season>/', views.team_goal_analysis_page, name='goal-analysis-page'),
    path('team-goal-search/', views.TeamSearchGoalView.as_view(), name='team-goal-search'),
    path('goal-chart/<team>/<season>/', views.team_goal_chart, name='goal-chart'),
    path('match-goal-search/', views.SearchGoalMatchView.as_view(), name='match-goal-search'),
    path('goal-search/', views.GoalDistView.as_view(), name='dist-goal-search'),

    path('export/', views.export_csv, name='export-csv'),
    path('update/', views.update_data, name='update-data'),
    path('f/', views.filter_data, name='filter-data'),
    path('delete/', views.delete_certain_data),
    path('result-page/', views.result_page, name='result-page'),
    path('pricing/', views.payment_page, name='payment-page'),

    path('search-form/', views.searchform, name='search-form'),
    path('search/', views.search_page, name='search'),
    path('club/<int:pk>/<str:slug>/', views.ClubDetailView.as_view(), name='club-detail'),
    path('s/', views.SearchView.as_view(), name='search-view'),
]

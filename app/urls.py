from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search-form/', views.searchform, name='search-form'),
    path('search/', views.search_page, name='search'),
    path('club/<int:pk>/<str:slug>/', views.ClubDetailView.as_view(), name='club-detail'),
    path('s/', views.SearchView.as_view(), name='search-view'),
    path('match-search/', views.SearchMatchView.as_view(), name='match-search'),
    path('pricing/', views.payment_page, name='payment-page'),
    path('export/', views.export_csv, name='export-csv'),
    path('update/', views.update_data, name='update-data'),
    path('result-page/', views.result_page, name='result-page'),
]

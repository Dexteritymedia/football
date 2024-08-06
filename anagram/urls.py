from django.urls import path

from . import views

app_name = 'anagram'

urlpatterns = [
    path('', views.home, name='home'),
    path('words-discovered/', views.word_result, name='results-page'),
]

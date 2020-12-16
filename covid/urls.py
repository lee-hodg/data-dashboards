from django.urls import path
from django.shortcuts import redirect

from . import views


urlpatterns = [
    path('', lambda request: redirect('index/', permanent=True)),
    path("index/", views.index, name="covid_index"),
    path("history/", views.history, name="covid_history"),
]

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("rankings/", views.rankings, name="rankings"),
    path("institutionRankings/", views.institutionRankings, name="institutionRankings"),
    path("round/", views.round, name="round"),
    path("generateOrder/", views.generateOrder, name="generateOrder"),
    path("teamList/", views.teamList, name="teamList")
]


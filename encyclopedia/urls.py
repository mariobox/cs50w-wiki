from django.urls import path
from . import views

#app_name = ""

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.article, name="article"),
    path("lookup/", views.lookup, name="lookup"),
    path("random/", views.random, name="random"),
    path("add/", views.add, name="add"),
    path("<str:title>/edit", views.edit, name="edit")
]

from django.urls import path
from .views import HomeView, PageDetailView, home_view

app_name = "core"

urlpatterns = [
    path("", home_view, name="home"),
    path("sayfa/<slug:slug>/", PageDetailView.as_view(), name="page_detail"),
] 
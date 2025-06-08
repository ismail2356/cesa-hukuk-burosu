from django.urls import path
from .views import HomeView, PageDetailView

app_name = "core"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("sayfa/<slug:slug>/", PageDetailView.as_view(), name="page_detail"),
] 
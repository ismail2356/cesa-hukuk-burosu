from django.urls import path
from . import views

app_name = 'lawyers'

urlpatterns = [
    path('', views.lawyer_list, name='lawyer_list'),
    path('debug/', views.debug_lawyers, name='debug_lawyers'),
    path('<slug:slug>/', views.lawyer_detail, name='lawyer_detail'),
] 
from django.urls import path
from .views import LawyerListView, LawyerDetailView

app_name = 'lawyers'

urlpatterns = [
    path('', LawyerListView.as_view(), name='lawyer_list'),
    path('<slug:slug>/', LawyerDetailView.as_view(), name='lawyer_detail'),
] 
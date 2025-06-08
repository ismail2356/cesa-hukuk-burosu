from django.urls import path
from .views import ContactView, OfficeLocationsView

app_name = 'contact'

urlpatterns = [
    path('', ContactView.as_view(), name='contact'),
    path('ofislerimiz/', OfficeLocationsView.as_view(), name='office_locations'),
] 
from django.urls import path
from .views import ServiceCategoryListView, ServiceCategoryDetailView, ServiceDetailView

app_name = 'services'

urlpatterns = [
    path('', ServiceCategoryListView.as_view(), name='service_category_list'),
    path('kategori/<slug:slug>/', ServiceCategoryDetailView.as_view(), name='service_category_detail'),
    path('hizmet/<slug:slug>/', ServiceDetailView.as_view(), name='service_detail'),
] 
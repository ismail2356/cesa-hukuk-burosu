from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import ServiceCategory, Service


class ServiceCategoryListView(ListView):
    """Hizmet kategorileri listesi görünümü"""
    model = ServiceCategory
    template_name = 'services/service_category_list.html'
    context_object_name = 'categories'
    
    def get_queryset(self):
        """Sadece aktif kategorileri listele"""
        return ServiceCategory.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Her kategori için aktif hizmetleri ekle
        for category in context['categories']:
            category.active_services = category.services.filter(is_active=True)
        return context


class ServiceCategoryDetailView(DetailView):
    """Hizmet kategorisi detay görünümü"""
    model = ServiceCategory
    template_name = 'services/service_category_detail.html'
    context_object_name = 'category'
    
    def get_queryset(self):
        """Sadece aktif kategorileri göster"""
        return ServiceCategory.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Bu kategorideki aktif hizmetleri ekle
        context['services'] = self.object.services.filter(is_active=True)
        return context


class ServiceDetailView(DetailView):
    """Hizmet detay görünümü"""
    model = Service
    template_name = 'services/service_detail.html'
    context_object_name = 'service'
    
    def get_queryset(self):
        """Sadece aktif hizmetleri göster"""
        return Service.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Aynı kategorideki diğer hizmetleri ekle
        context['related_services'] = Service.objects.filter(
            category=self.object.category,
            is_active=True
        ).exclude(id=self.object.id)[:4]
        return context

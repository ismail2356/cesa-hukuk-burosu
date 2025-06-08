from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from .models import Page
from apps.lawyers.models import Lawyer


class HomeView(TemplateView):
    """Ana sayfa görünümü"""
    template_name = "pages/home.html"


class PageDetailView(DetailView):
    """Sayfa detay görünümü"""
    model = Page
    template_name = "pages/page_detail.html"
    context_object_name = "page"
    
    def get_queryset(self):
        return Page.objects.filter(is_active=True)
    
    def get_template_names(self):
        """Özel sayfalar için özel şablonlar döndürür"""
        if self.object.slug == "hakkimizda":
            return ["pages/about.html"]
        # İleriki aşamalarda diğer özel sayfalar için şablonlar eklenebilir
        return [self.template_name]
    
    def get_context_data(self, **kwargs):
        """Şablona ek veriler ekler"""
        context = super().get_context_data(**kwargs)
        
        # Hakkımızda sayfası için en son eklenen 3 avukatı ekleyelim
        if self.object.slug == "hakkimizda":
            try:
                context['top_lawyers'] = Lawyer.objects.filter(is_active=True).order_by('-id')[:3]
            except:
                # Eğer avukatlar uygulaması henüz yoksa veya hata oluşursa, hata verme
                context['top_lawyers'] = []
                
        return context

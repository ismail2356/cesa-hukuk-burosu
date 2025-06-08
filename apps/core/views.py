from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from django.http import HttpResponse
from .models import Page
from apps.lawyers.models import Lawyer


def home_view(request):
    """Basit ana sayfa - debug için"""
    return HttpResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>CESA Hukuk Bürosu</title>
        <meta charset="utf-8">
        <style>
            body { font-family: Arial, sans-serif; text-align: center; margin: 50px; }
            .container { max-width: 600px; margin: 0 auto; }
            .btn { 
                background: #007bff; 
                color: white; 
                padding: 10px 20px; 
                text-decoration: none; 
                border-radius: 5px;
                display: inline-block;
                margin: 10px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎉 CESA Hukuk Bürosu</h1>
            <p>Website başarıyla çalışıyor!</p>
            <p>Deploy işlemi tamamlandı ve servis canlı durumda.</p>
            <a href="/admin" class="btn">Admin Panel</a>
            <a href="/iletisim" class="btn">İletişim</a>
        </div>
    </body>
    </html>
    """)


class HomeView(TemplateView):
    """Ana sayfa görünümü"""
    template_name = "pages/home_fixed.html"  # Çalışan güzel template


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

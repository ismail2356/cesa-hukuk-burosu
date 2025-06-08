from .models import SiteSettings, SEOMetaData


def site_settings(request):
    """Her şablona site ayarlarını ekler"""
    try:
        settings = SiteSettings.objects.first()
        return {'site_settings': settings}
    except:
        return {'site_settings': None}


def seo_meta(request):
    """Her şablona ilgili SEO meta verilerini ekler"""
    current_path = request.path
    
    try:
        # Önce tam URL eşleşmesi ara
        seo_data = SEOMetaData.objects.filter(target_url=current_path, is_active=True).first()
        
        if not seo_data:
            # Alternatif olarak, URL'nin bir kısmıyla eşleşen meta veri ara
            for meta in SEOMetaData.objects.filter(is_active=True):
                if meta.target_url in current_path:
                    seo_data = meta
                    break
        
        return {'seo_meta': seo_data}
    except:
        return {'seo_meta': None} 
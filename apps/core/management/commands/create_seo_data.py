from django.core.management.base import BaseCommand
from django.utils.text import slugify
from apps.core.models import SiteSettings, SEOMetaData


class Command(BaseCommand):
    help = 'Örnek SEO verileri oluşturur'

    def handle(self, *args, **options):
        # Site ayarlarını oluştur veya güncelle
        settings, created = SiteSettings.objects.get_or_create(
            pk=1,
            defaults={
                'site_name': 'CESA Hukuk Bürosu',
                'email': 'info@cesahukukdanismanlik.com',
                'phone': '+90 212 555 44 33',
                'address': 'Atatürk Bulvarı No:123, Bakırköy, İstanbul',
                'whatsapp': '+90 532 123 45 67',
            }
        )
        
        # SEO verilerini güncelle
        settings.meta_title = 'CESA Hukuk Bürosu | Profesyonel Hukuki Danışmanlık ve Avukatlık Hizmetleri'
        settings.meta_description = 'CESA Hukuk Bürosu, alanında uzman avukat kadrosuyla şirketlere ve bireylere kapsamlı hukuki danışmanlık hizmetleri sunmaktadır. İcra, boşanma, ticaret ve gayrimenkul hukuku alanlarında destek alın.'
        settings.meta_keywords = 'hukuk bürosu, avukat, hukuki danışmanlık, istanbul hukuk bürosu, icra avukatı, boşanma avukatı, ceza avukatı, ticaret hukuku, iş hukuku'
        settings.meta_author = 'CESA Hukuk Bürosu'
        settings.meta_copyright = '© 2023 CESA Hukuk Bürosu, Tüm Hakları Saklıdır.'
        settings.business_type = 'LegalService'
        settings.business_founded = '2015'
        settings.business_location_lat = '40.9712'
        settings.business_location_long = '28.8093'
        settings.business_opening_hours = 'Mo-Fr 09:00-18:00'
        settings.save()
        
        self.stdout.write(self.style.SUCCESS('Site ayarları ve SEO bilgileri güncellendi.'))
        
        # Örnek SEO Meta Verilerini Oluştur
        seo_pages = [
            {
                'title': 'Ana Sayfa',
                'target_url': '/',
                'meta_title': 'CESA Hukuk Bürosu | Profesyonel Hukuki Danışmanlık',
                'meta_description': 'CESA Hukuk Bürosu, İstanbul\'da şirketlere ve bireylere geniş yelpazede hukuki danışmanlık ve avukatlık hizmetleri sunan profesyonel bir hukuk bürosudur.',
                'meta_keywords': 'hukuk bürosu, avukat, istanbul avukat, hukuki danışmanlık, dava takibi, hukuk ofisi',
            },
            {
                'title': 'Hizmetlerimiz Sayfası',
                'target_url': '/hizmetler/',
                'meta_title': 'Hizmetlerimiz | CESA Hukuk Bürosu',
                'meta_description': 'CESA Hukuk Bürosu\'nun sunduğu geniş kapsamlı hukuki hizmetler: İcra ve İflas, Aile, Ticaret, İş, Gayrimenkul ve Ceza Hukuku alanlarında uzman avukatlarımız.',
                'meta_keywords': 'hukuki hizmetler, icra hukuku, iflas hukuku, aile hukuku, boşanma avukatı, ticaret hukuku, iş hukuku, gayrimenkul hukuku, ceza hukuku',
            },
            {
                'title': 'Avukatlarımız Sayfası',
                'target_url': '/avukatlar/',
                'meta_title': 'Avukatlarımız | CESA Hukuk Bürosu',
                'meta_description': 'CESA Hukuk Bürosu\'nda görev yapan uzman avukatlarımızı tanıyın. Her biri kendi alanında deneyimli ve donanımlı hukuk profesyonelleri.',
                'meta_keywords': 'istanbul avukatlar, uzman avukatlar, icra avukatı, boşanma avukatı, ceza avukatı, ticaret avukatı, hukuk danışmanları',
            },
            {
                'title': 'İcra Hukuku Kategorisi',
                'target_url': '/hizmetler/kategori/icra/',
                'meta_title': 'İcra ve İflas Hukuku | CESA Hukuk Bürosu',
                'meta_description': 'İcra ve iflas hukuku alanında uzman avukatlarımızla alacak tahsilatı, icra takibi, haciz işlemleri ve borç yapılandırma konularında hukuki destek sağlıyoruz.',
                'meta_keywords': 'icra hukuku, iflas hukuku, alacak tahsilatı, icra takibi, haciz işlemleri, borç yapılandırma, icra avukatı, icra davaları',
            },
            {
                'title': 'Aile Hukuku Kategorisi',
                'target_url': '/hizmetler/kategori/aile/',
                'meta_title': 'Aile Hukuku | CESA Hukuk Bürosu',
                'meta_description': 'Aile hukuku alanında uzman avukatlarımızla boşanma, nafaka, velayet, mal paylaşımı ve miras konularında hukuki danışmanlık hizmetleri sunuyoruz.',
                'meta_keywords': 'aile hukuku, boşanma, nafaka, velayet, çocuk teslimi, mal paylaşımı, boşanma avukatı, anlaşmalı boşanma, çekişmeli boşanma',
            },
            {
                'title': 'İletişim Sayfası',
                'target_url': '/iletisim/',
                'meta_title': 'İletişim | CESA Hukuk Bürosu',
                'meta_description': 'CESA Hukuk Bürosu ile iletişime geçin. İstanbul Bakırköy\'de bulunan ofisimize ulaşım bilgileri ve randevu talebi için bize ulaşın.',
                'meta_keywords': 'hukuk bürosu iletişim, avukat randevu, istanbul hukuk bürosu, bakırköy hukuk bürosu, cesahukukdanismanlik, hukuki danışmanlık iletişim',
            },
            {
                'title': 'Makaleler Sayfası',
                'target_url': '/makaleler/',
                'meta_title': 'Hukuki Makaleler | CESA Hukuk Bürosu',
                'meta_description': 'CESA Hukuk Bürosu avukatlarımızın kaleme aldığı güncel hukuki makaleler, bilgi notları ve hukuki değerlendirmeler.',
                'meta_keywords': 'hukuki makaleler, hukuk blogları, hukuki bilgi notları, güncel hukuk, kanun değişiklikleri, hukuki görüşler, dava örnekleri',
            },
        ]
        
        for page_data in seo_pages:
            SEOMetaData.objects.get_or_create(
                target_url=page_data['target_url'],
                defaults={
                    'title': page_data['title'],
                    'meta_title': page_data['meta_title'],
                    'meta_description': page_data['meta_description'],
                    'meta_keywords': page_data['meta_keywords'],
                    'og_title': page_data['meta_title'],
                    'og_description': page_data['meta_description'],
                    'is_active': True,
                }
            )
            
        self.stdout.write(self.style.SUCCESS(f'{len(seo_pages)} sayfa için SEO meta verileri oluşturuldu.')) 
#!/usr/bin/env python
import os
import sys
import django

# Django ayarlarını yükle
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.blog.models import Category, Tag, Article
from django.utils import timezone

def create_sample_data():
    """Örnek blog verileri oluştur"""
    
    # Admin kullanıcısını al
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        print("❌ Admin kullanıcısı bulunamadı!")
        return
    
    # Kategoriler oluştur
    categories_data = [
        {'name': 'Aile Hukuku', 'description': 'Boşanma, nafaka, velayet işlemleri'},
        {'name': 'İş Hukuku', 'description': 'İş sözleşmeleri, tazminat davaları'},
        {'name': 'Gayrimenkul Hukuku', 'description': 'Tapu işlemleri, kira sözleşmeleri'},
        {'name': 'Ceza Hukuku', 'description': 'Suç ve ceza işlemleri'},
        {'name': 'Ticaret Hukuku', 'description': 'Şirket kurulumu, ticari davalar'},
    ]
    
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description']}
        )
        if created:
            print(f"✅ Kategori oluşturuldu: {category.name}")
    
    # Etiketler oluştur
    tags_data = ['Boşanma', 'Nafaka', 'Velayet', 'İş Kazası', 'Tazminat', 'Tapu', 'Kira', 'Ceza', 'Şirket']
    
    for tag_name in tags_data:
        tag, created = Tag.objects.get_or_create(name=tag_name)
        if created:
            print(f"✅ Etiket oluşturuldu: {tag.name}")
    
    # Örnek makaleler oluştur
    articles_data = [
        {
            'title': 'Boşanma Davası Nasıl Açılır?',
            'category': 'Aile Hukuku',
            'summary': 'Boşanma davası açmak için gereken belgeler ve süreç hakkında bilgiler.',
            'content': '''Boşanma davası açmak isteyen eşlerin bilmesi gereken önemli konular vardır. 

Bu makalede boşanma davası sürecini detaylı olarak inceleyeceğiz:

1. Gerekli Belgeler
- Nüfus cüzdanı
- Evlilik cüzdanı  
- İkametgah belgesi

2. Dava Süreci
- Dilekçe hazırlama
- Mahkemeye başvuru
- Duruşma süreci

3. Masraflar
- Harç ve vekalet ücreti
- Mahkeme giderleri

Detaylı bilgi için hukuk büromuzla iletişime geçebilirsiniz.''',
            'tags': ['Boşanma']
        },
        {
            'title': 'İş Kazası Tazminat Hakları',
            'category': 'İş Hukuku',
            'summary': 'İş kazası sonucu alınabilecek tazminatlar ve başvuru süreçleri.',
            'content': '''İş kazası geçiren çalışanların tazminat hakları oldukça kapsamlıdır.

İş Kazası Tazminat Türleri:

1. Geçici İş Göremezlik Tazminatı
2. Sürekli İş Göremezlik Tazminatı  
3. Ölüm Tazminatı
4. Manevi Tazminat

Bu tazminatları alabilmek için gerekli şartlar ve başvuru süreçleri hakkında detaylı bilgi için uzman avukatlarımızla görüşün.''',
            'tags': ['İş Kazası', 'Tazminat']
        },
        {
            'title': 'Tapu İşlemleri Rehberi',
            'category': 'Gayrimenkul Hukuku', 
            'summary': 'Gayrimenkul alım satımında dikkat edilmesi gereken hukuki konular.',
            'content': '''Gayrimenkul alım satımı önemli bir yatırım kararıdır ve hukuki süreçlerin doğru yönetilmesi gerekir.

Tapu İşlemlerinde Dikkat Edilecekler:

1. Tapu Araştırması
- Tapu sicilinin incelenmesi
- İpotek ve haciz sorgulaması
- İmar durumu kontrolü

2. Satış Sözleşmesi
- Sözleşme şartları
- Ödeme planı
- Teslim koşulları

3. Vergi Yükümlülükleri
- Tapu harcı
- Emlak vergisi
- Gelir vergisi

Güvenli bir alım satım için mutlaka hukuki danışmanlık alın.''',
            'tags': ['Tapu']
        }
    ]
    
    for article_data in articles_data:
        # Kategoriyi bul
        category = Category.objects.get(name=article_data['category'])
        
        # Makaleyi oluştur
        article, created = Article.objects.get_or_create(
            title=article_data['title'],
            defaults={
                'author': admin_user,
                'category': category,
                'summary': article_data['summary'],
                'content': article_data['content'],
                'status': 'published',
                'published_at': timezone.now()
            }
        )
        
        if created:
            # Etiketleri ekle
            for tag_name in article_data['tags']:
                tag = Tag.objects.get(name=tag_name)
                article.tags.add(tag)
            
            print(f"✅ Makale oluşturuldu: {article.title}")
    
    print("\n🎉 Örnek blog verileri başarıyla oluşturuldu!")
    print(f"📊 Toplam: {Category.objects.count()} kategori, {Tag.objects.count()} etiket, {Article.objects.count()} makale")

if __name__ == '__main__':
    create_sample_data() 
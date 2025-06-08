from django.core.management.base import BaseCommand
from apps.core.models import Page


class Command(BaseCommand):
    help = 'Hakkımızda sayfasını oluşturur veya günceller'

    def handle(self, *args, **options):
        modern_content = """
        <!-- Ana İçerik -->
        <div class="row align-items-center mb-5">
            <div class="col-lg-6 mb-4 mb-lg-0" data-aos="fade-right">
                <div class="pe-lg-4">
                    <span class="badge bg-secondary fs-6 px-3 py-2 mb-3">15+ Yıllık Deneyim</span>
                    <h1 class="display-6 fw-bold text-primary mb-4">CESA Hukuk Bürosu</h1>
                    <p class="lead text-muted mb-4">
                        Hukukun evrensel ilkelerine bağlı kalarak, teknolojik gelişmeleri ve toplumsal dönüşümleri 
                        sürekli takip ediyor; her dosyamızda yüksek sorumluluk bilinciyle hareket ediyoruz.
                    </p>
                    <p class="mb-4">
                        Kurulduğumuz günden bu yana, <strong>adalete ve hukukun üstünlüğüne olan inancımızla</strong>, 
                        müvekkillerimizin hukuki süreçlerinde en iyi sonuçları elde etmek için çalışmaktayız. 
                        Büromuz, alanında uzmanlaşmış avukatlardan oluşan ekibiyle, her türlü hukuki sorununuzda 
                        yanınızda olmayı taahhüt etmektedir.
                    </p>
                    <div class="d-flex flex-wrap gap-3">
                        <a href="#hizmetler" class="btn btn-primary">
                            <i class="fas fa-balance-scale me-2"></i>Hizmet Alanları
                        </a>
                        <a href="#iletisim" class="btn btn-outline-primary">
                            <i class="fas fa-phone me-2"></i>İletişim
                        </a>
                    </div>
                </div>
            </div>
            <div class="col-lg-6" data-aos="fade-left">
                <div class="position-relative">
                    <div class="bg-light rounded-3 p-5 d-flex align-items-center justify-content-center" style="height: 400px;">
                        <div class="text-center">
                            <div class="feature-icon mx-auto mb-4" style="width: 120px; height: 120px;">
                                <i class="fas fa-balance-scale fa-4x text-primary"></i>
                            </div>
                            <h4 class="text-primary mb-2">Adalet ve Güven</h4>
                            <p class="text-muted">Müvekkillerimize hizmet vermenin gururunu yaşıyoruz</p>
                        </div>
                    </div>
                    <div class="position-absolute top-0 start-0 w-100 h-100 bg-primary opacity-10 rounded-3"></div>
                </div>
            </div>
        </div>

        <!-- Öne Çıkan Özellikler -->
        <div class="row g-4 mb-5">
            <div class="col-md-6 col-lg-3" data-aos="fade-up" data-aos-delay="100">
                <div class="card h-100 border-0 shadow-sm text-center">
                    <div class="card-body p-4">
                        <div class="feature-icon mx-auto mb-3">
                            <i class="fas fa-users text-primary"></i>
                        </div>
                        <h5 class="fw-bold mb-2">Uzman Kadro</h5>
                        <p class="text-muted small mb-0">15+ yıl deneyime sahip avukatlar</p>
                    </div>
                </div>
            </div>
            <div class="col-md-6 col-lg-3" data-aos="fade-up" data-aos-delay="200">
                <div class="card h-100 border-0 shadow-sm text-center">
                    <div class="card-body p-4">
                        <div class="feature-icon mx-auto mb-3">
                            <i class="fas fa-handshake text-primary"></i>
                        </div>
                        <h5 class="fw-bold mb-2">Güvenilirlik</h5>
                        <p class="text-muted small mb-0">Müvekkil memnuniyeti odaklı</p>
                    </div>
                </div>
            </div>
            <div class="col-md-6 col-lg-3" data-aos="fade-up" data-aos-delay="300">
                <div class="card h-100 border-0 shadow-sm text-center">
                    <div class="card-body p-4">
                        <div class="feature-icon mx-auto mb-3">
                            <i class="fas fa-shield-alt text-primary"></i>
                        </div>
                        <h5 class="fw-bold mb-2">Profesyonellik</h5>
                        <p class="text-muted small mb-0">Yüksek kalite standartları</p>
                    </div>
                </div>
            </div>
            <div class="col-md-6 col-lg-3" data-aos="fade-up" data-aos-delay="400">
                <div class="card h-100 border-0 shadow-sm text-center">
                    <div class="card-body p-4">
                        <div class="feature-icon mx-auto mb-3">
                            <i class="fas fa-clock text-primary"></i>
                        </div>
                        <h5 class="fw-bold mb-2">Hızlı Çözüm</h5>
                        <p class="text-muted small mb-0">Zamanında hukuki destek</p>
                    </div>
                </div>
            </div>
        </div>
        """

        page, created = Page.objects.get_or_create(
            slug='hakkimizda',
            defaults={
                'title': 'Hakkımızda',
                'content': modern_content,
                'meta_title': 'CESA Hukuk Bürosu | Hakkımızda - Profesyonel Hukuk Danışmanlığı',
                'meta_description': 'CESA Hukuk Bürosu hakkında bilgi alın. 15 yıllık deneyimle ceza, ticaret, aile, iş hukuku ve daha birçok alanda uzman hukuki danışmanlık hizmetleri.',
                'is_active': True
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'"{page.title}" sayfası başarıyla oluşturuldu.'))
        else:
            # Mevcut sayfayı güncelle
            page.content = modern_content
            page.meta_title = 'CESA Hukuk Bürosu | Hakkımızda - Profesyonel Hukuk Danışmanlığı'
            page.meta_description = 'CESA Hukuk Bürosu hakkında bilgi alın. 15 yıllık deneyimle ceza, ticaret, aile, iş hukuku ve daha birçok alanda uzman hukuki danışmanlık hizmetleri.'
            page.is_active = True
            page.save()
            self.stdout.write(self.style.SUCCESS(f'"{page.title}" sayfası güncellendi.')) 
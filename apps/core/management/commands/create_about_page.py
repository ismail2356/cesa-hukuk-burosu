from django.core.management.base import BaseCommand
from apps.core.models import Page


class Command(BaseCommand):
    help = 'Hakkımızda sayfasını oluşturur veya günceller'

    def handle(self, *args, **options):
        page, created = Page.objects.get_or_create(
            slug='hakkimizda',
            defaults={
                'title': 'Hakkımızda',
                'content': """
                <div class="mb-4">
                    <p class="lead text-primary fw-semibold">CESA Hukuk Bürosu, 15 yıllık deneyime sahip uzman kadrosuyla müvekkillerine kapsamlı hukuki danışmanlık ve dava hizmetleri sunmaktadır.</p>
                </div>

                <p>Kurulduğumuz günden bu yana, <strong>adalete ve hukukun üstünlüğüne olan inancımızla</strong>, müvekkillerimizin hukuki süreçlerinde en iyi sonuçları elde etmek için çalışmaktayız. Büromuz, alanında uzmanlaşmış avukatlardan oluşan ekibiyle, her türlü hukuki sorununuzda yanınızda olmayı taahhüt etmektedir.</p>

                <div class="row mt-4 mb-4">
                    <div class="col-md-6">
                        <div class="bg-light rounded p-3 h-100">
                            <h5 class="text-primary"><i class="fas fa-users me-2"></i>Deneyimli Kadro</h5>
                            <p class="mb-0 small">15+ yıl deneyime sahip uzman avukatlar</p>
                        </div>
                    </div>
                    <div class="col-md-6 mt-3 mt-md-0">
                        <div class="bg-light rounded p-3 h-100">
                            <h5 class="text-primary"><i class="fas fa-balance-scale me-2"></i>Geniş Hizmet Yelpazesi</h5>
                            <p class="mb-0 small">Hukukun her alanında profesyonel hizmet</p>
                        </div>
                    </div>
                </div>

                <h4 class="text-primary mt-4 mb-3">Hizmet Alanlarımız</h4>
                <p>CESA Hukuk Bürosu olarak aşağıdaki hukuk alanlarında uzman hizmet vermekteyiz:</p>

                <div class="row">
                    <div class="col-md-6">
                        <ul class="list-unstyled">
                            <li class="mb-2"><i class="fas fa-check text-primary me-2"></i><strong>Ceza Hukuku</strong></li>
                            <li class="mb-2"><i class="fas fa-check text-primary me-2"></i><strong>Ticaret Hukuku</strong></li>
                            <li class="mb-2"><i class="fas fa-check text-primary me-2"></i><strong>İş ve Sosyal Güvenlik Hukuku</strong></li>
                            <li class="mb-2"><i class="fas fa-check text-primary me-2"></i><strong>Aile Hukuku</strong></li>
                        </ul>
                    </div>
                    <div class="col-md-6">
                        <ul class="list-unstyled">
                            <li class="mb-2"><i class="fas fa-check text-primary me-2"></i><strong>Gayrimenkul ve İnşaat Hukuku</strong></li>
                            <li class="mb-2"><i class="fas fa-check text-primary me-2"></i><strong>Miras Hukuku</strong></li>
                            <li class="mb-2"><i class="fas fa-check text-primary me-2"></i><strong>Vergi Hukuku</strong></li>
                            <li class="mb-2"><i class="fas fa-check text-primary me-2"></i><strong>Yabancılar Hukuku</strong></li>
                        </ul>
                    </div>
                </div>

                <div class="alert alert-primary mt-4" role="alert">
                    <h5 class="alert-heading"><i class="fas fa-lightbulb me-2"></i>Yaklaşımımız</h5>
                    <p class="mb-0">Hukukun evrensel ilkelerine bağlı kalarak, teknolojik gelişmeleri ve toplumsal dönüşümleri sürekli takip ediyor; her dosyamızda yüksek sorumluluk bilinciyle hareket ediyoruz. Amacımız, yalnızca anlaşmazlıkları çözmek değil, aynı zamanda hukuki riskleri önceden tespit edip önleyici çözümler geliştirmektir.</p>
                </div>

                <p class="mt-4"><strong>CESA Hukuk Bürosu</strong> olarak, her müvekkilimizin davası bizim için önemlidir. Sizlere en iyi hizmeti sunmak için buradayız.</p>
                """,
                'meta_title': 'CESA Hukuk Bürosu | Hakkımızda - Profesyonel Hukuk Danışmanlığı',
                'meta_description': 'CESA Hukuk Bürosu hakkında bilgi alın. 15 yıllık deneyimle ceza, ticaret, aile, iş hukuku ve daha birçok alanda uzman hukuki danışmanlık hizmetleri.',
                'is_active': True
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'"{page.title}" sayfası başarıyla oluşturuldu.'))
        else:
            # Mevcut sayfayı güncelle
            page.content = """
            <div class="mb-4">
                <p class="lead text-primary fw-semibold">CESA Hukuk Bürosu, 15 yıllık deneyime sahip uzman kadrosuyla müvekkillerine kapsamlı hukuki danışmanlık ve dava hizmetleri sunmaktadır.</p>
            </div>

            <p>Kurulduğumuz günden bu yana, <strong>adalete ve hukukun üstünlüğüne olan inancımızla</strong>, müvekkillerimizin hukuki süreçlerinde en iyi sonuçları elde etmek için çalışmaktayız. Büromuz, alanında uzmanlaşmış avukatlardan oluşan ekibiyle, her türlü hukuki sorununuzda yanınızda olmayı taahhüt etmektedir.</p>

            <div class="row mt-4 mb-4">
                <div class="col-md-6">
                    <div class="bg-light rounded p-3 h-100">
                        <h5 class="text-primary"><i class="fas fa-users me-2"></i>Deneyimli Kadro</h5>
                        <p class="mb-0 small">15+ yıl deneyime sahip uzman avukatlar</p>
                    </div>
                </div>
                <div class="col-md-6 mt-3 mt-md-0">
                    <div class="bg-light rounded p-3 h-100">
                        <h5 class="text-primary"><i class="fas fa-balance-scale me-2"></i>Geniş Hizmet Yelpazesi</h5>
                        <p class="mb-0 small">Hukukun her alanında profesyonel hizmet</p>
                    </div>
                </div>
            </div>

            <h4 class="text-primary mt-4 mb-3">Hizmet Alanlarımız</h4>
            <p>CESA Hukuk Bürosu olarak aşağıdaki hukuk alanlarında uzman hizmet vermekteyiz:</p>

            <div class="row">
                <div class="col-md-6">
                    <ul class="list-unstyled">
                        <li class="mb-2"><i class="fas fa-check text-primary me-2"></i><strong>Ceza Hukuku</strong></li>
                        <li class="mb-2"><i class="fas fa-check text-primary me-2"></i><strong>Ticaret Hukuku</strong></li>
                        <li class="mb-2"><i class="fas fa-check text-primary me-2"></i><strong>İş ve Sosyal Güvenlik Hukuku</strong></li>
                        <li class="mb-2"><i class="fas fa-check text-primary me-2"></i><strong>Aile Hukuku</strong></li>
                    </ul>
                </div>
                <div class="col-md-6">
                    <ul class="list-unstyled">
                        <li class="mb-2"><i class="fas fa-check text-primary me-2"></i><strong>Gayrimenkul ve İnşaat Hukuku</strong></li>
                        <li class="mb-2"><i class="fas fa-check text-primary me-2"></i><strong>Miras Hukuku</strong></li>
                        <li class="mb-2"><i class="fas fa-check text-primary me-2"></i><strong>Vergi Hukuku</strong></li>
                        <li class="mb-2"><i class="fas fa-check text-primary me-2"></i><strong>Yabancılar Hukuku</strong></li>
                    </ul>
                </div>
            </div>

            <div class="alert alert-primary mt-4" role="alert">
                <h5 class="alert-heading"><i class="fas fa-lightbulb me-2"></i>Yaklaşımımız</h5>
                <p class="mb-0">Hukukun evrensel ilkelerine bağlı kalarak, teknolojik gelişmeleri ve toplumsal dönüşümleri sürekli takip ediyor; her dosyamızda yüksek sorumluluk bilinciyle hareket ediyoruz. Amacımız, yalnızca anlaşmazlıkları çözmek değil, aynı zamanda hukuki riskleri önceden tespit edip önleyici çözümler geliştirmektir.</p>
            </div>

            <p class="mt-4"><strong>CESA Hukuk Bürosu</strong> olarak, her müvekkilimizin davası bizim için önemlidir. Sizlere en iyi hizmeti sunmak için buradayız.</p>
            """
            page.meta_title = 'CESA Hukuk Bürosu | Hakkımızda - Profesyonel Hukuk Danışmanlığı'
            page.meta_description = 'CESA Hukuk Bürosu hakkında bilgi alın. 15 yıllık deneyimle ceza, ticaret, aile, iş hukuku ve daha birçok alanda uzman hukuki danışmanlık hizmetleri.'
            page.is_active = True
            page.save()
            self.stdout.write(self.style.SUCCESS(f'"{page.title}" sayfası güncellendi.')) 
from django.core.management.base import BaseCommand
from apps.core.models import Page


class Command(BaseCommand):
    help = 'Hakkımızda sayfasını oluşturur'

    def handle(self, *args, **options):
        if not Page.objects.filter(slug='hakkimizda').exists():
            page = Page.objects.create(
                title='Hakkımızda',
                slug='hakkimizda',
                content="""
                <h2>CESA Hukuk Bürosu Hakkında</h2>
                
                <p>CESA Hukuk Bürosu, 15 yıllık deneyime sahip uzman kadrosuyla müvekkillerine kapsamlı hukuki danışmanlık ve dava hizmetleri sunmaktadır.</p>
                
                <p>Kurulduğumuz günden bu yana, adalete ve hukukun üstünlüğüne olan inancımızla, müvekkillerimizin hukuki süreçlerinde en iyi sonuçları elde etmek için çalışmaktayız. Büromuz, alanında uzmanlaşmış avukatlardan oluşan ekibiyle, her türlü hukuki sorununuzda yanınızda olmayı taahhüt etmektedir.</p>
                
                <h3>Misyonumuz</h3>
                
                <p>Müvekkillerimizin hukuki ihtiyaçlarına en hızlı ve etkili çözümleri sunmak, hukuki haklarını en iyi şekilde savunmak ve onlara güven verici bir hukuk hizmeti sağlamaktır.</p>
                
                <h3>Vizyonumuz</h3>
                
                <p>Türkiye'nin önde gelen hukuk bürolarından biri olarak, müvekkillerimize uluslararası standartlarda hukuk hizmeti sunmak ve hukuk alanında öncü çalışmalara imza atmaktır.</p>
                
                <h3>Değerlerimiz</h3>
                
                <ul>
                    <li>Profesyonellik</li>
                    <li>Güvenilirlik</li>
                    <li>Şeffaflık</li>
                    <li>Dürüstlük</li>
                    <li>Müvekkil odaklılık</li>
                </ul>
                
                <p>CESA Hukuk Bürosu olarak, her müvekkilimizin davası bizim için önemlidir. Sizlere en iyi hizmeti sunmak için buradayız.</p>
                """,
                meta_title='CESA Hukuk Bürosu | Hakkımızda',
                meta_description='CESA Hukuk Bürosu, 15 yıllık deneyimiyle müvekkillerine kapsamlı hukuki danışmanlık ve dava hizmetleri sunmaktadır. Profesyonel ekibimizle yanınızdayız.',
                is_active=True
            )
            self.stdout.write(self.style.SUCCESS(f'"{page.title}" sayfası başarıyla oluşturuldu.'))
        else:
            self.stdout.write(self.style.WARNING('Hakkımızda sayfası zaten mevcut. İşlem yapılmadı.')) 
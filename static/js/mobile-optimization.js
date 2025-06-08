/**
 * CESA Hukuk Bürosu - Mobil Optimizasyon JS
 * Bu dosya, mobil kullanıcı deneyimini iyileştiren fonksiyonları içerir
 */

document.addEventListener('DOMContentLoaded', function() {
    // Navbar scroll etkisi için güçlendirilmiş kod
    const navbar = document.querySelector('.navbar');
    
    function updateNavbarClass() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    }
    
    // Sayfa yüklendiğinde pozisyona göre navbar sınıfını ayarla
    updateNavbarClass();
    
    // Scroll olayında navbar sınıfını güncelle - pasif olay kullanarak performans artışı
    window.addEventListener('scroll', updateNavbarClass, {passive: true});
    
    // Mobil dokunma alanları için iyileştirme
    const touchItems = document.querySelectorAll('a, button, .btn, .nav-link');
    touchItems.forEach(item => {
        // Dokunmatik cihazlar için hover durumunu iyileştir
        item.addEventListener('touchstart', function() {
            this.classList.add('active-touch');
        }, {passive: true});
        
        item.addEventListener('touchend', function() {
            this.classList.remove('active-touch');
        }, {passive: true});
    });
    
    // Form gönderimini iyileştirme
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        // Form gönderildiğinde butonun yükleniyor durumunu göster
        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                // Butonun orijinal içeriğini sakla
                const originalContent = submitBtn.innerHTML;
                // Yükleniyor simgesini göster
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span> Gönderiliyor...';
                submitBtn.disabled = true;
                
                // 10 saniye sonra butonu eski haline getir (eğer form zaten gönderilmediyse)
                setTimeout(() => {
                    if (submitBtn.disabled) {
                        submitBtn.innerHTML = originalContent;
                        submitBtn.disabled = false;
                    }
                }, 10000);
            }
        });
    });
    
    // Performans iyileştirmeleri için görsel yükleme optimizasyonu
    const lazyImages = document.querySelectorAll('img[loading="lazy"]');
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        lazyImages.forEach(img => {
            imageObserver.observe(img);
        });
    } else {
        // IntersectionObserver desteklenmiyor, basit yükleme yap
        lazyImages.forEach(img => {
            img.src = img.dataset.src;
        });
    }
    
    // Mobil menü kapanma efekti
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
        document.addEventListener('click', function(event) {
            const isClickInside = navbarToggler.contains(event.target) || navbarCollapse.contains(event.target);
            
            if (!isClickInside && navbarCollapse.classList.contains('show')) {
                // Navbar dışına tıklandığında menüyü kapat
                navbarToggler.click();
            }
        });
    }
    
    // Hızlı telefon erişimi butonu için scroll etki
    const quickContact = document.querySelector('.quick-contact');
    if (quickContact) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 300) {
                quickContact.classList.add('visible');
            } else {
                quickContact.classList.remove('visible');
            }
        }, {passive: true});
    }
}); 
/**
 * CESA Hukuk Bürosu - Form Validasyonu
 * Bu dosya, formlar için client-side validasyon sağlar.
 */

// Gerçek zamanlı doğrulama işlemleri için gerekli fonksiyonlar
document.addEventListener('DOMContentLoaded', function() {
    const contactForm = document.getElementById('contact-form-element');
    const appointmentForm = document.getElementById('appointment-form-element');

    // Regex tanımlamaları
    const patterns = {
        email: /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/,
        phone: /^[0-9]{10,11}$/,
        fullName: /^[a-zA-ZçÇğĞıİöÖşŞüÜ\s]{3,50}$/,
        subject: /^[a-zA-Z0-9çÇğĞıİöÖşŞüÜ\s.,!?()]{3,100}$/,
    };

    // Input doğrulama fonksiyonu
    function validateInput(input, pattern) {
        const value = input.value.trim();
        const isValid = pattern ? pattern.test(value) : value.length > 0;
        
        if (isValid) {
            input.classList.remove('is-invalid');
            input.classList.add('is-valid');
            return true;
        } else {
            input.classList.remove('is-valid');
            input.classList.add('is-invalid');
            return false;
        }
    }

    // Hata mesajları
    const errorMessages = {
        'full_name': 'Lütfen geçerli bir ad soyad giriniz (en az 3 karakter).',
        'email': 'Lütfen geçerli bir e-posta adresi giriniz.',
        'phone': 'Lütfen geçerli bir telefon numarası giriniz (10-11 rakam).',
        'subject': 'Konu en az 3 karakter olmalıdır.',
        'message': 'Lütfen bir mesaj giriniz.',
        'preferred_date': 'Lütfen tarih seçiniz.',
        'preferred_time': 'Lütfen saat seçiniz.'
    };

    // Hata mesajı gösteren fonksiyon
    function showErrorMessage(input, message) {
        const feedbackDiv = input.parentElement.querySelector('.invalid-feedback');
        if (!feedbackDiv) {
            const div = document.createElement('div');
            div.className = 'invalid-feedback';
            div.textContent = message;
            input.parentElement.appendChild(div);
        } else {
            feedbackDiv.textContent = message;
        }
    }

    // Input olayı her bir form elemanı için
    function setupInputValidation(form) {
        if (!form) return;

        const inputs = form.querySelectorAll('input, textarea');
        
        inputs.forEach(input => {
            // Otomatik hata mesajı ekle
            const fieldName = input.name;
            if (errorMessages[fieldName]) {
                showErrorMessage(input, errorMessages[fieldName]);
            }

            // Her input değiştiğinde validasyon yap
            input.addEventListener('input', function() {
                let pattern = null;
                
                if (fieldName === 'full_name') {
                    pattern = patterns.fullName;
                } else if (fieldName === 'email') {
                    pattern = patterns.email;
                } else if (fieldName === 'phone') {
                    pattern = patterns.phone;
                } else if (fieldName === 'subject') {
                    pattern = patterns.subject;
                }
                
                validateInput(this, pattern);
            });

            // Blur olduğunda validasyon yap
            input.addEventListener('blur', function() {
                let pattern = null;
                
                if (fieldName === 'full_name') {
                    pattern = patterns.fullName;
                } else if (fieldName === 'email') {
                    pattern = patterns.email;
                } else if (fieldName === 'phone') {
                    pattern = patterns.phone;
                } else if (fieldName === 'subject') {
                    pattern = patterns.subject;
                }
                
                validateInput(this, pattern);
            });
        });
    }

    // Form gönderilmeden önce validasyon
    function setupFormSubmission(form, formId) {
        if (!form) return;

        form.addEventListener('submit', function(e) {
            let isValid = true;
            const inputs = form.querySelectorAll('input, textarea');
            
            inputs.forEach(input => {
                let pattern = null;
                const fieldName = input.name;
                
                if (fieldName === 'full_name') {
                    pattern = patterns.fullName;
                } else if (fieldName === 'email') {
                    pattern = patterns.email;
                } else if (fieldName === 'phone') {
                    pattern = patterns.phone;
                } else if (fieldName === 'subject') {
                    pattern = patterns.subject;
                }
                
                if (!validateInput(input, pattern)) {
                    isValid = false;
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                // Form üzerinde ilk hatayı bul ve o alana scroll yap
                const firstInvalid = form.querySelector('.is-invalid');
                if (firstInvalid) {
                    firstInvalid.focus();
                    firstInvalid.scrollIntoView({
                        behavior: 'smooth',
                        block: 'center'
                    });
                }
                
                // Hata mesajı göster
                const formAlert = document.createElement('div');
                formAlert.className = 'alert alert-danger mt-3';
                formAlert.textContent = 'Lütfen formdaki hataları düzeltin ve tekrar deneyin.';
                
                // Önceki hata mesajı varsa kaldır
                const existingAlert = form.querySelector('.alert');
                if (existingAlert) {
                    existingAlert.remove();
                }
                
                form.prepend(formAlert);
            } else {
                // Başarılı mesajı göster
                const loadingMessage = document.createElement('div');
                loadingMessage.className = 'alert alert-info mt-3';
                loadingMessage.textContent = 'Formunuz gönderiliyor, lütfen bekleyin...';
                
                // Önceki mesajları kaldır
                const existingAlerts = form.querySelectorAll('.alert');
                existingAlerts.forEach(alert => alert.remove());
                
                form.prepend(loadingMessage);
            }
        });
    }

    // Formları yapılandır
    setupInputValidation(contactForm);
    setupInputValidation(appointmentForm);
    setupFormSubmission(contactForm, 'contact-form');
    setupFormSubmission(appointmentForm, 'appointment-form');
}); 
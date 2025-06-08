from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView, ListView
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from .models import ContactMessage, OfficeLocation
from .forms import ContactForm


class ContactView(View):
    """İletişim sayfası görünümü"""
    template_name = 'contact/contact.html'
    
    def get(self, request):
        context = {
            'contact_form': ContactForm(),
            'office_locations': OfficeLocation.objects.filter(is_active=True).order_by('order'),
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact = contact_form.save()
            
            # E-posta gönderimi
            try:
                subject = f"CESA Hukuk Bürosu - Yeni İletişim Mesajı: {contact.subject}"
                message = f"Ad Soyad: {contact.full_name}\n" \
                          f"E-posta: {contact.email}\n" \
                          f"Telefon: {contact.phone}\n" \
                          f"Konu: {contact.subject}\n\n" \
                          f"Mesaj:\n{contact.message}"
                
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [settings.CONTACT_EMAIL]
                
                send_mail(subject, message, from_email, recipient_list)
                
            except Exception as e:
                print(f"E-posta gönderim hatası: {e}")
            
            messages.success(request, 'Mesajınız başarıyla gönderildi. En kısa sürede size dönüş yapacağız.')
            return redirect('contact:contact')
        else:
            messages.error(request, 'Lütfen formu doğru şekilde doldurun.')
            return render(request, self.template_name, {
                'contact_form': contact_form,
                'office_locations': OfficeLocation.objects.filter(is_active=True).order_by('order'),
            })


class OfficeLocationsView(ListView):
    """Ofis lokasyonları listesi görünümü"""
    model = OfficeLocation
    template_name = 'contact/office_locations.html'
    context_object_name = 'office_locations'
    
    def get_queryset(self):
        """Sadece aktif lokasyonları listele"""
        return OfficeLocation.objects.filter(is_active=True).order_by('order')

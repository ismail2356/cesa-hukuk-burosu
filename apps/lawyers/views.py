from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Lawyer


def lawyer_list(request):
    """Avukatlar listesi görünümü"""
    lawyers = Lawyer.objects.filter(is_active=True)
    return render(request, 'lawyers/lawyer_list.html', {'lawyers': lawyers})


def lawyer_detail(request, slug):
    """Avukat detay görünümü"""
    lawyer = get_object_or_404(Lawyer, slug=slug, is_active=True)
    return render(request, 'lawyers/lawyer_detail.html', {'lawyer': lawyer})


def debug_lawyers(request):
    """Debug görünümü"""
    lawyers = Lawyer.objects.all()
    return render(request, 'lawyers/debug_lawyers.html', {'lawyers': lawyers})


class LawyerListView(ListView):
    """Avukatlar listesi görünümü"""
    model = Lawyer
    template_name = 'lawyers/lawyer_list.html'
    context_object_name = 'lawyers'
    
    def get_queryset(self):
        """Sadece aktif avukatları listele"""
        return Lawyer.objects.filter(is_active=True)


class LawyerDetailView(DetailView):
    """Avukat detay görünümü"""
    model = Lawyer
    template_name = 'lawyers/lawyer_detail.html'
    context_object_name = 'lawyer'
    
    def get_queryset(self):
        """Sadece aktif avukatları göster"""
        return Lawyer.objects.filter(is_active=True)

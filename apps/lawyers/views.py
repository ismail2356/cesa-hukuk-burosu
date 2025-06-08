from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Lawyer


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

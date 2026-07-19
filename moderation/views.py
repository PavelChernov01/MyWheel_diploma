from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

from cars.models import CarListing


@staff_member_required
def moderation_list(request):
    """Список объявлений на модерации"""
    moderation_list = CarListing.objects.filter(status='moderation').order_by('-created_at')
    active_list = CarListing.objects.filter(status='active').order_by('-created_at')[:10]

    context = {
        'moderation_list': moderation_list,
        'active_list': active_list,
        'moderation_count': moderation_list.count(),
    }
    return render(request, 'moderation/list.html', context)


@staff_member_required
def moderation_approve(request, pk):
    """Одобрить объявление"""
    car = get_object_or_404(CarListing, pk=pk, status='moderation')
    car.status = 'active'
    car.save()
    messages.success(request, f'Объявление "{car.brand.name} {car.model.name}" одобрено')
    return redirect('moderation_list')


@staff_member_required
def moderation_reject(request, pk):
    """Отклонить объявление"""
    car = get_object_or_404(CarListing, pk=pk, status='moderation')
    car.status = 'rejected'
    car.save()
    messages.success(request, f'Объявление "{car.brand.name} {car.model.name}" отклонено')
    return redirect('moderation_list')
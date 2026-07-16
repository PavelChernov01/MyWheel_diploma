from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Favorite
from .serializers import FavoriteSerializer
from cars.models import CarListing


# ============ API Views ============

class FavoriteListCreateView(generics.ListCreateAPIView):
    """Список избранных и добавление в избранное"""
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        listing_id = self.request.data.get('listing_id')
        listing = get_object_or_404(CarListing, id=listing_id)
        serializer.save(user=self.request.user, listing=listing)


class FavoriteDeleteView(generics.DestroyAPIView):
    """Удаление из избранного"""
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)


# ============ HTML Views (без JavaScript) ============

@login_required
def favorites_list(request):
    """Страница со списком избранных объявлений"""
    favorites = Favorite.objects.filter(user=request.user).select_related('listing__brand', 'listing__model')
    return render(request, 'favorites/list.html', {'favorites': favorites})


@login_required
def favorites_add(request, pk):
    """Добавление в избранное (через GET)"""
    car = get_object_or_404(CarListing, pk=pk)
    favorite, created = Favorite.objects.get_or_create(user=request.user, listing=car)
    if created:
        messages.success(request, f'Объявление "{car.brand.name} {car.model.name}" добавлено в избранное')
    else:
        messages.info(request, 'Объявление уже в избранном')
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def favorites_remove(request, pk):
    """Удаление из избранного (через GET)"""
    favorite = get_object_or_404(Favorite, pk=pk, user=request.user)
    car_name = f"{favorite.listing.brand.name} {favorite.listing.model.name}"
    favorite.delete()
    messages.success(request, f'Объявление "{car_name}" удалено из избранного')
    return redirect('favorites_list')
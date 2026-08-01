from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg

from .models import Review
from .serializers import ReviewSerializer, ReviewCreateSerializer
from cars.models import CarListing


# ============ API Views ============

class ReviewListCreateView(generics.ListCreateAPIView):
    """Список отзывов на объявление и создание отзыва"""
    serializer_class = ReviewCreateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        listing_id = self.kwargs.get('listing_id')
        return Review.objects.filter(listing_id=listing_id, is_moderated=True)

    def perform_create(self, serializer):
        listing = get_object_or_404(CarListing, id=self.kwargs.get('listing_id'))
        serializer.save(listing=listing)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Детальный просмотр, редактирование, удаление отзыва"""
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Review.objects.all()

    def perform_update(self, serializer):
        serializer.save()


# ============ HTML Views ============

@login_required
def review_create(request, pk):
    """Создание отзыва (через GET)"""
    listing = get_object_or_404(CarListing, pk=pk)

    # Проверки
    if request.user == listing.user:
        messages.error(request, 'Вы не можете оставить отзыв на своё объявление')
        return redirect('car_detail', pk=pk)

    if Review.objects.filter(reviewer=request.user, listing=listing).exists():
        messages.error(request, 'Вы уже оставили отзыв на это объявление')
        return redirect('car_detail', pk=pk)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        if not rating or not comment:
            messages.error(request, 'Пожалуйста, заполните все поля')
            return redirect('car_detail', pk=pk)

        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                raise ValueError
        except ValueError:
            messages.error(request, 'Оценка должна быть от 1 до 5')
            return redirect('car_detail', pk=pk)

        Review.objects.create(
            reviewer=request.user,
            seller=listing.user,
            listing=listing,
            rating=rating,
            comment=comment,
            is_moderated=True  # Для диплома сразу публикуем
        )

        messages.success(request, 'Ваш отзыв успешно добавлен!')
        return redirect('car_detail', pk=pk)

    return render(request, 'reviews/create.html', {'listing': listing})

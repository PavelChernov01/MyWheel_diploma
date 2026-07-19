from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction

from .models import CarListing, CarImage
from .serializers import (
    CarListingSerializer, CarListingDetailSerializer,
    CarListingCreateSerializer
)
from .filters import CarListingFilter
from .forms import CarListingForm, MultipleCarImageForm
from reviews.models import Review  # Добавлено


# ============ API Views ============

class CarListingListView(generics.ListAPIView):
    """Список объявлений с фильтрацией и поиском"""
    serializer_class = CarListingSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CarListingFilter
    search_fields = ['description', 'brand__name', 'model__name', 'city']
    ordering_fields = ['price', 'year', 'created_at', 'views_count']
    ordering = ['-created_at']

    def get_queryset(self):
        return CarListing.objects.filter(status='active').select_related('brand', 'model', 'user')


class CarListingDetailView(generics.RetrieveAPIView):
    """Детальный просмотр объявления"""
    serializer_class = CarListingDetailSerializer
    queryset = CarListing.objects.filter(status='active')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views_count += 1
        instance.save(update_fields=['views_count'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CarListingCreateView(generics.CreateAPIView):
    """Создание объявления"""
    serializer_class = CarListingCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CarListingUpdateView(generics.UpdateAPIView):
    """Обновление объявления"""
    serializer_class = CarListingCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CarListing.objects.filter(user=self.request.user)


class CarListingDeleteView(generics.DestroyAPIView):
    """Удаление объявления"""
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CarListing.objects.filter(user=self.request.user)


# ============ HTML Views (фронтенд) ============

def car_list(request):
    """Главная страница со списком объявлений"""
    cars = CarListing.objects.filter(status='active').order_by('-created_at')
    return render(request, 'cars/list.html', {'cars': cars})


def car_detail(request, pk):
    """Детальная страница объявления"""
    car = get_object_or_404(CarListing, pk=pk, status='active')
    car.views_count += 1
    car.save(update_fields=['views_count'])

    # Отзывы
    reviews = Review.objects.filter(listing=car, is_moderated=True).order_by('-created_at')
    user_review = None
    if request.user.is_authenticated:
        user_review = Review.objects.filter(listing=car, reviewer=request.user).first()

    context = {
        'car': car,
        'reviews': reviews,
        'user_review': user_review,
    }
    return render(request, 'cars/detail.html', context)


@login_required
def car_create(request):
    """Создание объявления"""
    if request.method == 'POST':
        form = CarListingForm(request.POST)
        image_form = MultipleCarImageForm(request.POST, request.FILES)

        if form.is_valid():
            with transaction.atomic():
                car = form.save(commit=False)
                car.user = request.user
                car.status = 'moderation'
                car.save()

                # Обработка изображений
                images = request.FILES.getlist('images')
                for i, image in enumerate(images):
                    CarImage.objects.create(
                        listing=car,
                        image=image,
                        is_main=(i == 0),
                        order=i
                    )

            messages.success(request, 'Объявление создано и отправлено на модерацию!')
            return redirect('car_detail', pk=car.pk)
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме')
    else:
        form = CarListingForm()
        image_form = MultipleCarImageForm()

    return render(request, 'cars/create.html', {
        'form': form,
        'image_form': image_form,
    })
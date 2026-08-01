from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.core.cache import cache

from .models import CarListing, CarImage
from .serializers import (
    CarListingSerializer, CarListingDetailSerializer,
    CarListingCreateSerializer
)
from .filters import CarListingFilter
from .forms import CarListingForm, MultipleCarImageForm
from reviews.models import Review
from brands.models import Brand


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

    page_number = request.GET.get('page', 1)

    # ============ КЕШИРОВАНИЕ СПИСКА ОБЪЯВЛЕНИЙ ============
    cache_key_cars = f'car_list_page_{page_number}'
    cars = cache.get(cache_key_cars)

    if cars is None:
        cars_list = CarListing.objects.filter(status='active').order_by('-created_at')
        paginator = Paginator(cars_list, 9)
        cars = paginator.get_page(page_number)
        cache.set(cache_key_cars, cars, 300)  # 5 минут
        print(f"💰 Объявления (страница {page_number}) сохранены в кеш")
    else:
        print(f"💰 Объявления (страница {page_number}) загружены из кеша")

    # ============ КЕШИРОВАНИЕ СТАТИСТИКИ ============
    stats = cache.get('homepage_stats')

    if stats is None:
        stats = {
            'cars_count': CarListing.objects.filter(status='active').count(),
            'brands_count': Brand.objects.count(),
            'cities_count': CarListing.objects.filter(status='active').values('city').distinct().count(),
            'users_count': get_user_model().objects.count(),
        }
        cache.set('homepage_stats', stats, 3600)  # 1 час
        print("💰 Статистика сохранена в кеш")
    else:
        print("💰 Статистика загружена из кеша")

    context = {
        'cars': cars,
        'cars_count': stats['cars_count'],
        'brands_count': stats['brands_count'],
        'cities_count': stats['cities_count'],
        'users_count': stats['users_count'],
    }
    return render(request, 'cars/list.html', context)


def car_detail(request, pk):
    """Детальная страница объявления"""

    # ============ КЕШИРОВАНИЕ ДЕТАЛЬНОЙ СТРАНИЦЫ ============
    cache_key = f'car_detail_{pk}'
    car = cache.get(cache_key)

    if car is None:
        car = get_object_or_404(CarListing, pk=pk)
        cache.set(cache_key, car, 3600)  # 1 час
        print(f"💰 Детальная страница авто {pk} сохранена в кеш")
    else:
        print(f"💰 Детальная страница авто {pk} загружена из кеша")

    if car.status != 'active' and car.user != request.user:
        from django.http import Http404
        raise Http404("Объявление не найдено")

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
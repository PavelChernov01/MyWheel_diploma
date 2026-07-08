from django.db import models
from django.conf import settings
from django.contrib.postgres.search import SearchVectorField
from core.models import BaseModel
from brands.models import Brand, Model, BodyType, EngineType, TransmissionType, DriveType


class CarListing(BaseModel):
    """Объявление о продаже автомобиля"""

    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('moderation', 'На модерации'),
        ('active', 'Активно'),
        ('sold', 'Продано'),
        ('archived', 'Архивировано'),
        ('rejected', 'Отклонено'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='listings',
        verbose_name='Продавец'
    )
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE,
        related_name='listings', verbose_name='Марка'
    )
    model = models.ForeignKey(
        Model, on_delete=models.CASCADE,
        related_name='listings', verbose_name='Модель'
    )

    year = models.PositiveIntegerField(verbose_name='Год выпуска')
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Цена')
    mileage = models.PositiveIntegerField(verbose_name='Пробег, км')

    body_type = models.ForeignKey(
        BodyType, on_delete=models.SET_NULL,
        null=True, verbose_name='Тип кузова'
    )
    engine_type = models.ForeignKey(
        EngineType, on_delete=models.SET_NULL,
        null=True, verbose_name='Тип двигателя'
    )
    transmission = models.ForeignKey(
        TransmissionType, on_delete=models.SET_NULL,
        null=True, verbose_name='КПП'
    )
    drive_type = models.ForeignKey(
        DriveType, on_delete=models.SET_NULL,
        null=True, verbose_name='Тип привода'
    )

    engine_volume = models.DecimalField(
        max_digits=4, decimal_places=1,
        blank=True, null=True, verbose_name='Объём двигателя, л'
    )
    horsepower = models.PositiveIntegerField(
        blank=True, null=True, verbose_name='Мощность, л.с.'
    )

    color = models.CharField(max_length=50, blank=True, null=True, verbose_name='Цвет')
    vin = models.CharField(max_length=17, blank=True, null=True, verbose_name='VIN-код')
    description = models.TextField(verbose_name='Описание')

    city = models.CharField(max_length=100, verbose_name='Город')
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name='Адрес')

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='moderation',
        verbose_name='Статус'
    )

    published_at = models.DateTimeField(blank=True, null=True, verbose_name='Дата публикации')
    sold_at = models.DateTimeField(blank=True, null=True, verbose_name='Дата продажи')

    views_count = models.PositiveIntegerField(default=0, verbose_name='Количество просмотров')
    favorites_count = models.PositiveIntegerField(default=0, verbose_name='В избранном')

    search_vector = SearchVectorField(null=True, blank=True, verbose_name='Поисковый вектор')

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['brand', 'model']),
            models.Index(fields=['price']),
            models.Index(fields=['search_vector']),
        ]

    def __str__(self):
        return f"{self.brand.name} {self.model.name} - {self.year} - {self.price} руб."

    @property
    def is_active(self):
        return self.status == 'active'

    def publish(self):
        from django.utils import timezone
        self.status = 'active'
        self.published_at = timezone.now()
        self.save()


class CarImage(BaseModel):
    """Изображения автомобиля"""
    listing = models.ForeignKey(
        CarListing,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Объявление'
    )
    image = models.ImageField(upload_to='cars/%Y/%m/%d/', verbose_name='Изображение')
    is_main = models.BooleanField(default=False, verbose_name='Основное изображение')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')
    hash = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"Изображение #{self.id} к {self.listing.id}"

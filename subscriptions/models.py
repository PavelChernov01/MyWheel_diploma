from django.db import models
from django.conf import settings
from core.models import BaseModel
from brands.models import Brand, Model


class Subscription(BaseModel):
    """Подписка на поисковые критерии"""

    FREQUENCY_CHOICES = [
        ('instant', 'Мгновенно'),
        ('daily', 'Раз в день'),
        ('weekly', 'Раз в неделю'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Пользователь'
    )

    # Критерии поиска
    brand = models.ForeignKey(
        Brand, on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name='Марка'
    )
    model = models.ForeignKey(
        Model, on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name='Модель'
    )

    min_price = models.DecimalField(
        max_digits=12, decimal_places=2,
        null=True, blank=True,
        verbose_name='Цена от'
    )
    max_price = models.DecimalField(
        max_digits=12, decimal_places=2,
        null=True, blank=True,
        verbose_name='Цена до'
    )

    min_year = models.PositiveIntegerField(
        null=True, blank=True,
        verbose_name='Год от'
    )
    max_year = models.PositiveIntegerField(
        null=True, blank=True,
        verbose_name='Год до'
    )

    city = models.CharField(
        max_length=100,
        null=True, blank=True,
        verbose_name='Город'
    )

    frequency = models.CharField(
        max_length=20,
        choices=FREQUENCY_CHOICES,
        default='instant',
        verbose_name='Частота'
    )

    is_active = models.BooleanField(default=True, verbose_name='Активна')
    last_notified_at = models.DateTimeField(
        null=True, blank=True,
        verbose_name='Последнее уведомление'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ['-created_at']

    def __str__(self):
        return f"Подписка #{self.id} - {self.user.email}"

    def get_search_params(self):
        """Возвращает параметры поиска в виде словаря"""
        params = {}
        if self.brand_id:
            params['brand'] = self.brand_id
        if self.model_id:
            params['model'] = self.model_id
        if self.min_price:
            params['price__gte'] = self.min_price
        if self.max_price:
            params['price__lte'] = self.max_price
        if self.min_year:
            params['year__gte'] = self.min_year
        if self.max_year:
            params['year__lte'] = self.max_year
        if self.city:
            params['city'] = self.city
        params['status'] = 'active'
        return params

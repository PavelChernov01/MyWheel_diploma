from django.db import models
from django.conf import settings
from core.models import BaseModel
from cars.models import CarListing


class Favorite(BaseModel):
    """Избранное объявление"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )
    listing = models.ForeignKey(
        CarListing,
        on_delete=models.CASCADE,
        related_name='favorited_by',
        verbose_name='Объявление'
    )
    price_at_add = models.DecimalField(
        max_digits=12, decimal_places=2,
        blank=True, null=True,
        verbose_name='Цена при добавлении'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        unique_together = ['user', 'listing']

    def __str__(self):
        return f"{self.user.email} -> {self.listing}"

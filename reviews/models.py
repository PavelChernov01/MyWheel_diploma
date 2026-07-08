from django.db import models
from django.conf import settings
from core.models import BaseModel
from cars.models import CarListing


class Review(BaseModel):
    """Отзыв о продавце"""
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='given_reviews',
        verbose_name='Автор отзыва'
    )
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_reviews',
        verbose_name='Продавец'
    )
    listing = models.ForeignKey(
        CarListing,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Объявление'
    )
    rating = models.PositiveSmallIntegerField(
        choices=[(i, i) for i in range(1, 6)],
        verbose_name='Оценка'
    )
    comment = models.TextField(verbose_name='Комментарий')
    is_moderated = models.BooleanField(default=False, verbose_name='Промодерирован')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        unique_together = ['reviewer', 'listing']

    def __str__(self):
        return f"{self.reviewer.email} -> {self.seller.email}: {self.rating}★"

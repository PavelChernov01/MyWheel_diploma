from django.contrib.auth.models import AbstractUser
from django.db import models
from core.models import BaseModel


class User(BaseModel, AbstractUser):
    """Расширенная модель пользователя"""
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Телефон')
    avatar = models.ImageField(upload_to='avatars/%Y/%m/', blank=True, null=True, verbose_name='Аватар')
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name='Город')

    is_verified = models.BooleanField(default=False, verbose_name='Email подтверждён')
    is_blocked = models.BooleanField(default=False, verbose_name='Заблокирован')

    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0, verbose_name='Рейтинг')
    total_reviews = models.PositiveIntegerField(default=0, verbose_name='Количество отзывов')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-created_at']
        db_table = 'accounts_user'

    def __str__(self):
        return f"{self.email} ({self.first_name} {self.last_name})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username

from django.db import models
from core.models import BaseModel


class Brand(BaseModel):
    """Марка автомобиля"""
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    logo = models.ImageField(upload_to='brands/', blank=True, null=True, verbose_name='Логотип')
    country = models.CharField(max_length=100, blank=True, null=True, verbose_name='Страна')
    is_active = models.BooleanField(default=True, verbose_name='Активна')

    class Meta:
        verbose_name = 'Марка'
        verbose_name_plural = 'Марки'

    def __str__(self):
        return self.name


class Model(BaseModel):
    """Модель автомобиля"""
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='models', verbose_name='Марка')
    name = models.CharField(max_length=100, verbose_name='Название модели')
    year_start = models.PositiveIntegerField(blank=True, null=True, verbose_name='Год выпуска (с)')
    year_end = models.PositiveIntegerField(blank=True, null=True, verbose_name='Год выпуска (по)')
    is_active = models.BooleanField(default=True, verbose_name='Активна')

    class Meta:
        verbose_name = 'Модель'
        verbose_name_plural = 'Модели'
        unique_together = ['brand', 'name']

    def __str__(self):
        return f"{self.brand.name} {self.name}"


class BodyType(BaseModel):
    """Тип кузова"""
    name = models.CharField(max_length=50, unique=True, verbose_name='Тип кузова')
    code = models.CharField(max_length=20, unique=True, verbose_name='Код')
    icon = models.CharField(max_length=50, blank=True, null=True, verbose_name='Иконка')

    class Meta:
        verbose_name = 'Тип кузова'
        verbose_name_plural = 'Типы кузова'

    def __str__(self):
        return self.name


class EngineType(BaseModel):
    """Тип двигателя"""
    name = models.CharField(max_length=50, unique=True, verbose_name='Тип двигателя')
    code = models.CharField(max_length=20, unique=True, verbose_name='Код')

    class Meta:
        verbose_name = 'Тип двигателя'
        verbose_name_plural = 'Типы двигателя'

    def __str__(self):
        return self.name


class TransmissionType(BaseModel):
    """Тип коробки передач"""
    name = models.CharField(max_length=50, unique=True, verbose_name='Тип КПП')
    code = models.CharField(max_length=20, unique=True, verbose_name='Код')

    class Meta:
        verbose_name = 'Тип КПП'
        verbose_name_plural = 'Типы КПП'

    def __str__(self):
        return self.name


class DriveType(BaseModel):
    """Тип привода"""
    name = models.CharField(max_length=50, unique=True, verbose_name='Тип привода')
    code = models.CharField(max_length=20, unique=True, verbose_name='Код')

    class Meta:
        verbose_name = 'Тип привода'
        verbose_name_plural = 'Типы привода'

    def __str__(self):
        return self.name

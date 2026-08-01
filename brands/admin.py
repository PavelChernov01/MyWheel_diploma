from django.contrib import admin
from .models import Brand, Model, BodyType, EngineType, TransmissionType, DriveType

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'is_active')
    search_fields = ('name',)

@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    list_display = ('brand', 'name', 'year_start', 'year_end')
    list_filter = ('brand',)

@admin.register(BodyType)
class BodyTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')

@admin.register(EngineType)
class EngineTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')

@admin.register(TransmissionType)
class TransmissionTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')

@admin.register(DriveType)
class DriveTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')

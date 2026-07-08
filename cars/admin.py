from django.contrib import admin
from .models import CarListing, CarImage

class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 3

@admin.register(CarListing)
class CarListingAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'year', 'price', 'status', 'user', 'created_at')
    list_filter = ('status', 'brand', 'year')
    search_fields = ('brand__name', 'model__name', 'description')
    inlines = [CarImageInline]
    readonly_fields = ('views_count',)

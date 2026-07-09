from django_filters import rest_framework as filters
from .models import CarListing


class CarListingFilter(filters.FilterSet):
    """Фильтр для объявлений"""

    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')

    min_year = filters.NumberFilter(field_name='year', lookup_expr='gte')
    max_year = filters.NumberFilter(field_name='year', lookup_expr='lte')

    min_mileage = filters.NumberFilter(field_name='mileage', lookup_expr='gte')
    max_mileage = filters.NumberFilter(field_name='mileage', lookup_expr='lte')

    brand_name = filters.CharFilter(field_name='brand__name', lookup_expr='icontains')
    model_name = filters.CharFilter(field_name='model__name', lookup_expr='icontains')
    city = filters.CharFilter(field_name='city', lookup_expr='icontains')

    class Meta:
        model = CarListing
        fields = [
            'brand', 'model', 'body_type', 'engine_type',
            'transmission', 'drive_type', 'status', 'city',
            'min_price', 'max_price', 'min_year', 'max_year',
            'min_mileage', 'max_mileage'
        ]
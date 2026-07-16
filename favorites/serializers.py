from rest_framework import serializers
from .models import Favorite
from cars.serializers import CarListingSerializer


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор для избранного"""
    listing = CarListingSerializer(read_only=True)
    listing_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Favorite
        fields = ('id', 'user', 'listing', 'listing_id', 'created_at')
        read_only_fields = ('id', 'user', 'created_at')
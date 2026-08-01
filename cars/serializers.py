from rest_framework import serializers
from .models import CarListing, CarImage


class CarImageSerializer(serializers.ModelSerializer):
    """Сериализатор для изображений"""

    class Meta:
        model = CarImage
        fields = ('id', 'image', 'is_main', 'order')


class CarListingSerializer(serializers.ModelSerializer):
    """Сериализатор для списка объявлений"""
    images = CarImageSerializer(many=True, read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.full_name', read_only=True)

    class Meta:
        model = CarListing
        fields = (
            'id', 'user', 'user_email', 'user_name',
            'brand', 'model', 'year', 'price', 'mileage',
            'body_type', 'engine_type', 'transmission', 'drive_type',
            'engine_volume', 'horsepower',
            'color', 'description', 'city',
            'status', 'created_at', 'updated_at',
            'views_count', 'favorites_count', 'images'
        )
        read_only_fields = ('id', 'user', 'created_at', 'updated_at', 'views_count', 'favorites_count')


class CarListingDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для детального просмотра"""
    images = CarImageSerializer(many=True, read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    user_rating = serializers.DecimalField(source='user.rating', read_only=True, max_digits=3, decimal_places=2)

    class Meta:
        model = CarListing
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_at', 'updated_at', 'views_count', 'favorites_count')


class CarListingCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания объявления"""
    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = CarListing
        fields = (
            'brand', 'model', 'year', 'price', 'mileage',
            'body_type', 'engine_type', 'transmission', 'drive_type',
            'engine_volume', 'horsepower', 'color', 'description', 'city',
            'images'
        )

    def create(self, validated_data):
        images = validated_data.pop('images', [])
        validated_data['user'] = self.context['request'].user
        validated_data['status'] = 'moderation'

        listing = CarListing.objects.create(**validated_data)

        for i, image in enumerate(images):
            CarImage.objects.create(
                listing=listing,
                image=image,
                is_main=(i == 0),
                order=i
            )

        return listing
from rest_framework import serializers
from .models import Review
from accounts.serializers import UserProfileSerializer


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов"""
    reviewer_name = serializers.SerializerMethodField()
    seller_name = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ('id', 'reviewer', 'reviewer_name', 'seller', 'seller_name',
                  'listing', 'rating', 'comment', 'is_moderated', 'created_at')
        read_only_fields = ('id', 'reviewer', 'created_at', 'is_moderated')

    def get_reviewer_name(self, obj):
        return obj.reviewer.full_name or obj.reviewer.username

    def get_seller_name(self, obj):
        return obj.seller.full_name or obj.seller.username


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания отзыва"""

    class Meta:
        model = Review
        fields = ('listing', 'rating', 'comment')

    def validate(self, data):
        request = self.context.get('request')
        listing = data.get('listing')

        # Проверяем, что пользователь не оставляет отзыв сам себе
        if request.user == listing.user:
            raise serializers.ValidationError("Нельзя оставить отзыв на своё объявление")

        # Проверяем, что пользователь уже оставлял отзыв на это объявление
        if Review.objects.filter(reviewer=request.user, listing=listing).exists():
            raise serializers.ValidationError("Вы уже оставили отзыв на это объявление")

        return data

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['reviewer'] = request.user
        validated_data['seller'] = validated_data['listing'].user
        return super().create(validated_data)
from django.contrib import admin
from .models import Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'brand', 'model', 'min_price', 'max_price', 'is_active', 'frequency')
    list_filter = ('is_active', 'frequency')
    search_fields = ('user__email', 'brand__name', 'model__name')
    readonly_fields = ('created_at', 'updated_at')

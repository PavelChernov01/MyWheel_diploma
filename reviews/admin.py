from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('reviewer', 'seller', 'rating', 'is_moderated', 'created_at')
    list_filter = ('rating', 'is_moderated')
    search_fields = ('reviewer__email', 'seller__email', 'comment')
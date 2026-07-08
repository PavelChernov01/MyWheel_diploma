from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'phone', 'is_active', 'is_verified')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    list_filter = ('is_active', 'is_verified', 'is_staff')

    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {
            'fields': ('phone', 'avatar', 'city', 'is_verified', 'rating', 'total_reviews'),
        }),
    )
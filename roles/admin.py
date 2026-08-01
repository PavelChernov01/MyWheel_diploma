from django.contrib import admin
from .models import Role, RolePermission, UserRole

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_system')
    search_fields = ('name', 'code')
    list_filter = ('is_system',)

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'assigned_by', 'expires_at')
    list_filter = ('role',)
    search_fields = ('user__email',)

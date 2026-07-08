from django.db import models
from django.contrib.auth.models import Permission
from core.models import BaseModel
from accounts.models import User


class Role(BaseModel):
    """Роль пользователя"""
    name = models.CharField(max_length=100, unique=True, verbose_name='Название роли')
    code = models.CharField(max_length=50, unique=True, verbose_name='Код роли')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    permissions = models.ManyToManyField(
        Permission,
        through='RolePermission',
        related_name='roles',
        verbose_name='Разрешения'
    )
    is_system = models.BooleanField(default=False, verbose_name='Системная роль')

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'

    def __str__(self):
        return self.name


class RolePermission(BaseModel):
    """Связь роли и разрешения"""
    role = models.ForeignKey(Role, on_delete=models.CASCADE, verbose_name='Роль')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, verbose_name='Разрешение')
    is_granted = models.BooleanField(default=True, verbose_name='Разрешено')

    class Meta:
        verbose_name = 'Разрешение роли'
        verbose_name_plural = 'Разрешения ролей'
        unique_together = ['role', 'permission']

    def __str__(self):
        return f"{self.role.name} - {self.permission.name}"


class UserRole(BaseModel):
    """Связь пользователя и роли"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_roles', verbose_name='Пользователь')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='user_roles', verbose_name='Роль')
    assigned_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        related_name='assigned_roles', verbose_name='Назначил'
    )
    expires_at = models.DateTimeField(blank=True, null=True, verbose_name='Действует до')

    class Meta:
        verbose_name = 'Роль пользователя'
        verbose_name_plural = 'Роли пользователей'
        unique_together = ['user', 'role']

    def __str__(self):
        return f"{self.user.email} - {self.role.name}"
from django.db import models
from django.conf import settings
from core.models import BaseModel


class AuditLog(BaseModel):
    """Лог действий пользователей"""

    ACTION_CHOICES = [
        ('login', 'Вход в систему'),
        ('logout', 'Выход из системы'),
        ('create', 'Создание'),
        ('update', 'Обновление'),
        ('delete', 'Удаление'),
        ('view', 'Просмотр'),
        ('publish', 'Публикация'),
        ('archive', 'Архивация'),
        ('moderate', 'Модерация'),
        ('role_assign', 'Назначение роли'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='audit_logs',
        verbose_name='Пользователь'
    )
    action = models.CharField(
        max_length=50,
        choices=ACTION_CHOICES,
        verbose_name='Действие'
    )
    model_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Модель'
    )
    object_id = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='ID объекта'
    )
    object_repr = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Представление объекта'
    )
    data = models.JSONField(
        null=True,
        blank=True,
        verbose_name='Данные'
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        verbose_name='IP-адрес'
    )
    user_agent = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='User-Agent'
    )

    class Meta:
        verbose_name = 'Лог аудита'
        verbose_name_plural = 'Логи аудита'
        ordering = ['-created_at']
        db_table = 'audit_auditlog'

    def __str__(self):
        user_str = self.user.email if self.user else 'Аноним'
        return f"{user_str} - {self.get_action_display()} - {self.model_name} #{self.object_id}"
from audit.models import AuditLog


class AuditMiddleware:
    """Middleware для логирования действий пользователей"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Логируем запросы к API (кроме статики и админки)
        path = request.path
        excluded_paths = ['/admin/', '/static/', '/media/', '/api/docs/']

        if not any(path.startswith(p) for p in excluded_paths):
            if request.user and request.user.is_authenticated:
                # Логируем только изменяющие действия (POST, PUT, DELETE)
                if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
                    AuditLog.objects.create(
                        user=request.user,
                        action=self.get_action_from_method(request.method),
                        model_name=request.path.split('/')[-2] if len(request.path.split('/')) > 2 else '',
                        ip_address=self.get_client_ip(request),
                        user_agent=request.META.get('HTTP_USER_AGENT', ''),
                        data={
                            'method': request.method,
                            'path': request.path,
                        }
                    )

        return response

    def get_action_from_method(self, method):
        """Определяет тип действия по методу HTTP"""
        mapping = {
            'POST': 'create',
            'PUT': 'update',
            'PATCH': 'update',
            'DELETE': 'delete',
        }
        return mapping.get(method, 'view')

    def get_client_ip(self, request):
        """Получает IP-адрес клиента"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
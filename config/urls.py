from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from cars.views import car_list, car_detail, car_create

urlpatterns = [
    path('', car_list, name='home'),  # Теперь главная страница — список объявлений
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),
    path('car/<int:pk>/', car_detail, name='car_detail'),
    path('car/create/', car_create, name='car_create'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
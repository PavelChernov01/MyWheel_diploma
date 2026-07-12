from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from cars.views import car_list, car_detail, car_create
from accounts.views import login_view, logout_view, register_view

urlpatterns = [
    path('', car_list, name='home'),
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),

    # Страницы сайта
    path('car/<int:pk>/', car_detail, name='car_detail'),
    path('car/create/', car_create, name='car_create'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
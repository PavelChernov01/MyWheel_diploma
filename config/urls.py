from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from cars.views import car_list, car_detail, car_create
from accounts.views import login_view, logout_view, register_view, profile_view
from favorites.views import favorites_list, favorites_add, favorites_remove
from moderation.views import moderation_list, moderation_approve, moderation_reject

urlpatterns = [
    path('', car_list, name='home'),
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),
    path('reviews/', include('reviews.urls')),

    # Модерация (прямые маршруты)
    path('moderation/', moderation_list, name='moderation_list'),
    path('moderation/approve/<int:pk>/', moderation_approve, name='moderation_approve'),
    path('moderation/reject/<int:pk>/', moderation_reject, name='moderation_reject'),

    # Страницы сайта
    path('car/<int:pk>/', car_detail, name='car_detail'),
    path('car/create/', car_create, name='car_create'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('profile/', profile_view, name='profile'),

    # Избранное
    path('favorites/', favorites_list, name='favorites_list'),
    path('favorites/add/<int:pk>/', favorites_add, name='favorites_add'),
    path('favorites/remove/<int:pk>/', favorites_remove, name='favorites_remove'),

    # Восстановление пароля
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='accounts/password_reset.html',
             email_template_name='accounts/password_reset_email.html',
             subject_template_name='accounts/password_reset_subject.txt'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from accounts.views import (
    RegisterView, LoginView, ProfileView,
    ProfileUpdateView, LogoutView
)
from cars.views import (
    CarListingListView, CarListingDetailView,
    CarListingCreateView, CarListingUpdateView,
    CarListingDeleteView
)

app_name = 'api'

urlpatterns = [
    # Аутентификация
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/profile/', ProfileView.as_view(), name='profile'),
    path('auth/profile/update/', ProfileUpdateView.as_view(), name='profile_update'),

    # Объявления
    path('cars/', CarListingListView.as_view(), name='cars_list'),
    path('cars/create/', CarListingCreateView.as_view(), name='cars_create'),
    path('cars/<int:pk>/', CarListingDetailView.as_view(), name='cars_detail'),
    path('cars/<int:pk>/update/', CarListingUpdateView.as_view(), name='cars_update'),
    path('cars/<int:pk>/delete/', CarListingDeleteView.as_view(), name='cars_delete'),
]
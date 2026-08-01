from django.urls import path
from .views import ReviewListCreateView, ReviewDetailView, review_create

app_name = 'reviews'

urlpatterns = [
    path('api/listing/<int:listing_id>/reviews/', ReviewListCreateView.as_view(), name='api_review_list'),
    path('api/reviews/<int:pk>/', ReviewDetailView.as_view(), name='api_review_detail'),
    path('create/<int:pk>/', review_create, name='review_create'),
]
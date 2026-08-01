from django.urls import path
from .views import moderation_list, moderation_approve, moderation_reject

app_name = 'moderation'

urlpatterns = [
    path('', moderation_list, name='moderation_list'),
    path('approve/<int:pk>/', moderation_approve, name='moderation_approve'),
    path('reject/<int:pk>/', moderation_reject, name='moderation_reject'),
]
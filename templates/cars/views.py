from django.http import Http404
from reviews.models import Review

def car_detail(request, pk):
    """Детальная страница объявления"""
    # Показываем объявление, если оно активно ИЛИ если пользователь является владельцем
    car = get_object_or_404(CarListing, pk=pk)

    # Если объявление не активно и пользователь не владелец — 404
    if car.status != 'active' and car.user != request.user:
        raise Http404("Объявление не найдено")

    car.views_count += 1
    car.save(update_fields=['views_count'])

    # Отзывы
    reviews = Review.objects.filter(listing=car, is_moderated=True).order_by('-created_at')
    user_review = None
    if request.user.is_authenticated:
        user_review = Review.objects.filter(listing=car, reviewer=request.user).first()

    context = {
        'car': car,
        'reviews': reviews,
        'user_review': user_review,
    }
    return render(request, 'cars/detail.html', context)
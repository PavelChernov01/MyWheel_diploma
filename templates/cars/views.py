def car_list(request):
    """Главная страница со списком объявлений"""
    cars = CarListing.objects.filter(status='active').order_by('-created_at')

    context = {
        'cars': cars,
        'cars_count': CarListing.objects.filter(status='active').count(),
        'brands_count': Brand.objects.count(),
        'cities_count': CarListing.objects.filter(status='active').values('city').distinct().count(),
        'users_count': get_user_model().objects.count(),
    }
    return render(request, 'cars/list.html', context)
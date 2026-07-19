from django.shortcuts import render


def about_view(request):
    return render(request, 'pages/about.html')


def contacts_view(request):
    return render(request, 'pages/contacts.html')


def help_view(request):
    return render(request, 'pages/help.html')
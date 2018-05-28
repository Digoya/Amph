from django.shortcuts import render


def categories(request):
    return render(request, 'categories.html')


def authors(request):
    return render(request, 'authors.html')

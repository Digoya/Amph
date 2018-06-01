from django.shortcuts import render
from journal.models import UserProfile




def categories(request):
    return render(request, 'categories.html')


def authors(request):
    author_list = UserProfile.objects.order_by('user__username')[:5]
    content = {'author_list': author_list}
    return render(request, 'authors.html', content)

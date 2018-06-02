from django.shortcuts import render, get_object_or_404
from journal.models import UserProfile, Article
from django.core import exceptions
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpRequest


def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        auth_login(request, user)
        return redirect(author, author_username=username)
    else:
        return render(request, 'login.html')


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def categories(request):
    return render(request, 'categories.html')


def authors(request):
    author_list = UserProfile.objects.order_by('user__username')[:5]
    content = {'author_list': author_list,
               }
    return render(request, 'authors.html', content)


def author(request, author_username):
    try:
        get_author = get_object_or_404(UserProfile, user__username=author_username)
        sub_amount = UserProfile.objects.filter(subscribed__user__username__exact=author_username).count()
        articles = Article.objects.filter(author=get_author)
    except exceptions.ObjectDoesNotExist:
        get_author = None
    content = {'author': get_author,
               'sub_amount': sub_amount,
               'articles': articles,
               }
    return render(request, 'profile.html', content)

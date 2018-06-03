from django.shortcuts import render, get_object_or_404
from journal.models import UserProfile, Article, EmailVerification
from django.core import exceptions
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponseRedirect, HttpRequest
from django.core.mail import send_mail
import hashlib


def email_check(request, email_key):
    email = EmailVerification.objects.get(email_key=email_key)
    if email is None:
        return render(request, 'base.html', {'content': 'Something went wrong'})
    else:
        user_email = email.email
        email.delete()
        return render(request, '', {'content': 'Your email has confirmed'})


def email_sighup(request):
    email = request.POST.get('email')
    user_email = EmailVerification(email=email, email_key=hashlib.md5(email.encode()).hexdigest())
    user_email.save()
    send_mail('Amph Email',
              'http://127.0.0.1:8000/email-verification/' + hashlib.md5(email.encode('utf-8')).hexdigest(),
              'amph.response@gmail.com',
              [email],
              fail_silently=False,
              )
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        auth_login(request, user)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
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

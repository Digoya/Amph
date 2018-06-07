from django.shortcuts import render, get_object_or_404
from journal.models import *
from django.core import exceptions
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponseRedirect, HttpRequest, HttpResponseForbidden, Http404, HttpResponse, \
    HttpResponseBadRequest
from django.core.mail import send_mail
from journal.forms import RegistrationForm, SettingsForm
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from django.utils.cache import iri_to_uri
import hashlib
import urllib.parse as decoder
import json


def check(request):
    form = RegistrationForm()
    return render(request, 'registration.html', context={'form': form})


# Registration view


def sign_up(request):
    form = RegistrationForm(request.POST)
    if form.is_valid():
        user = User(username=form.cleaned_data['username'],
                    password=make_password(form.cleaned_data['password']),
                    email=form.cleaned_data['email'])
        user.save()
        new_user = UserProfile(user=user)
        new_user.short_describe = form.cleaned_data['describe_yourself']
        new_user.save()
        EmailVerification.objects.get(email=form.cleaned_data['email']).delete()
        return HttpResponseRedirect('/categories/')


# Take url with hashed email and checks existence in db


def email_check(request, email_key):
    email_instance = EmailVerification.objects.get(email_key=email_key)
    user_instance = UserProfile.objects.filter(user__email=email_instance.email).exists()
    if email_instance is None or user_instance:
        return render(request, 'base.html', {'content': 'This email already taken or invalid'})
    else:
        form = RegistrationForm(initial={'email': email_instance.email})
        return render(request, 'registration.html', {'form': form})


# Sends letter with link to confirm user email


def email_signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        validator = EmailValidator()
        try:
            validator(email)
        except ValidationError:
            raise HttpResponseBadRequest
        user_email = EmailVerification(email=email, email_key=hashlib.md5(email.encode()).hexdigest())
        user_email.save()
        send_mail('Amph Email',
                  'Please confirm your email: http://127.0.0.1:8000/email-verification/' + hashlib.md5(
                      email.encode('utf-8')).hexdigest(),
                  'amph.response@gmail.com',
                  [email],
                  fail_silently=False,
                  )
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        # return HttpResponse(
        #     json.dumps({'email': email}),
        #     content_type='application/json',
        # )
    else:
        raise HttpResponseBadRequest


# Checks login and password and authenticate the user


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return HttpResponseRedirect(reverse('author', args=(username,)))
        else:
            return render(request, 'login.html')
    return HttpResponse(request, 'User or Password is incorrect')


# Logout user


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# Shows Categories


def categories(request):
    return render(request, 'categories.html')


# Shows authors


def authors(request):
    author_list = UserProfile.objects.order_by('user__username')[:5]
    content = {'author_list': author_list,
               }
    return render(request, 'authors.html', content)


# Shows certain profile


def author(request, author_username):
    try:
        get_author = get_object_or_404(UserProfile, user__username=author_username)
        sub_amount = UserProfile.objects.filter(subscribed__user__username__exact=author_username).count()
        journals = Journal.objects.filter(author=get_author)
    except exceptions.ObjectDoesNotExist:
        get_author = None
    content = {'author': get_author,
               'sub_amount': sub_amount,
               'journals': journals,
               }
    return render(request, 'profile.html', content)


def journal(request, author_username, journal_name):
    journal_instance = Journal.objects.get(journal_name=journal_name.replace("_", " "))
    articles = Article.objects.filter(journal__journal_name=journal_name.replace("_", " "))
    content = {'author': author_username,
               'journal': journal_instance,
               'articles': articles,
               }
    return render(request, 'journal.html', content)


def article(request, author_username, journal_name, article_name):
    article_instance = Article.objects.get(title=article_name.replace("_", " "))
    content = {'article': article_instance,
               'author': author_username,
               'journal_name': journal_name,
               }
    return render(request, 'article.html', content)


def settings(request):
    if request.user.is_authenticated:
        user = UserProfile.objects.get(user__username=request.user.username)
        form = SettingsForm(initial={'username': user.user.username,
                                     'describe_yourself': user.short_describe,
                                     'gender': user.gender,
                                     'birth_year': user.birth_year,
                                     'email': user.user.email,
                                     })
        return render(request, 'settings.html', {'form': form})
    else:
        return render(request, 'login.html')


def save_changes(request):
    if request.user.is_authenticated:
        user = UserProfile.objects.get(user__username=request.user)
        form = SettingsForm(request.POST)
        if form.is_valid():
            user.user.username = form.cleaned_data['username']
            if make_password(form.cleaned_data['old_password']) == user.user.password and form.cleaned_data[
                'new_password'] != '':
                user.user.password = make_password(form.cleaned_data['new_password'])
            user.user.email = form.cleaned_data['email']
            user.save()
            user.short_describe = form.cleaned_data['describe_yourself']
            user.birth_year = form.cleaned_data['birth_year']
            user.gender = form.cleaned_data['gender']
            user.save()
            return HttpResponseRedirect('/authors/' + user.user.username + '/settings/')

    else:
        return render(request, 'login.html')

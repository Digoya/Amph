from django.shortcuts import render, get_object_or_404, redirect
from journal.models import *
from django.core import exceptions
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponseRedirect, HttpRequest, HttpResponseForbidden, Http404, HttpResponse, \
    HttpResponseBadRequest, JsonResponse
from django.core.mail import send_mail
from journal.forms import RegistrationForm, SettingsForm, CreateArticle, CreateJournal
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from django.utils.cache import iri_to_uri
import hashlib
import urllib.parse as decoder
import json


# Check registration form
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
    if request.method == 'POST' and not request.user.is_authenticated:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return HttpResponseRedirect(reverse('author', args=(username,)))
    return render(request, 'login.html')


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
    is_sub = False
    try:
        get_author = get_object_or_404(UserProfile, user__username=author_username)
        sub_amount = UserProfile.objects.filter(subscribed__user__username__exact=author_username).count()
        journals = Journal.objects.filter(author=get_author)
        if request.user.is_authenticated:
            is_sub = UserProfile.objects.get(user=request.user).subscribed.filter(
                user__username=author_username).exists()
    except exceptions.ObjectDoesNotExist:
        get_author = None
    content = {'author': get_author,
               'sub_amount': sub_amount,
               'journals': journals,
               'is_sub': is_sub,
               }
    return render(request, 'profile.html', content)


# Shows profile journals
def journal(request, author_username, journal_name):
    journal_instance = Journal.objects.get(journal_name=journal_name.replace("_", " "))
    articles = Article.objects.filter(journal__journal_name=journal_name.replace("_", " "))
    content = {'author': author_username,
               'journal': journal_instance,
               'articles': articles,
               }
    return render(request, 'journal.html', content)


# Manage your Journals and Articles
def create(request, author_username, action, journal_name='', article_name=''):
    if action == "create-journal" and request.user.is_authenticated:
        form = CreateJournal(initial={'new': "True"})
        return render(request, 'create-journal.html', {'form': form})
    elif action == "edit-journal" and journal_name != '' and request.user.is_authenticated:
        edit_journal = Journal.objects.get(journal_name=journal_name.replace("_", " "),
                                           author=UserProfile.objects.get(user=request.user))
        form = CreateJournal(initial={'journal_name': edit_journal.journal_name,
                                      'short_disc': edit_journal.short_disc,
                                      'new': "False",
                                      'old_name': edit_journal.journal_name})
        return render(request, 'create-journal.html', {'form': form, 'is_new': False})
    elif action == "save-journal" and request.method == 'POST' and request.user.is_authenticated:
        input_form = CreateJournal(request.POST, request.FILES)
        if input_form.is_valid():
            if input_form.cleaned_data['new'] == "True":
                journal = Journal(journal_name=input_form.cleaned_data['journal_name'],
                                  author=UserProfile.objects.get(user__username=request.user.username),
                                  short_disc=input_form.cleaned_data['short_disc'],
                                  avatar=input_form.cleaned_data['avatar'])
                journal.save()
            else:
                journal_instance = Journal.objects.get(
                    journal_name=input_form.cleaned_data['old_name'],
                    author=UserProfile.objects.get(user__username=request.user.username), )
                journal_instance.journal_name = input_form.cleaned_data['journal_name']
                journal_instance.short_disc = input_form.cleaned_data['short_disc']
                if input_form.cleaned_data['avatar'] is not None:
                    journal_instance.avatar = input_form.cleaned_data['avatar']
                journal_instance.save()
            return HttpResponseRedirect('/authors/' + request.user.username)
    elif action == "delete-journal" and request.user.is_authenticated and journal_name != '':
        try:
            Journal.objects.get(author=UserProfile.objects.get(user=request.user),
                                journal_name=journal_name.replace("_", " ")).delete()
        except exceptions.ObjectDoesNotExist:
            return HttpResponseBadRequest
        return HttpResponseRedirect('/authors/' + request.user.username)
    elif action == "create-article" and journal_name != '' and request.user.is_authenticated:
        form = CreateArticle(initial={'journal': journal_name,
                                      'new': "True"})
        return render(request, 'create-article.html', {'form': form, 'is_new': True})
    elif action == "edit-article" and journal_name != '' and request.user.is_authenticated:
        edit_article = Article.objects.get(journal__journal_name=journal_name.replace("_", " "),
                                           title=article_name.replace("_", " "),
                                           author=UserProfile.objects.get(user=request.user))
        form = CreateArticle(initial={'journal': journal_name,
                                      'article_name': edit_article.title,
                                      'article_short_desk': edit_article.short_desc,
                                      'article_body': edit_article.body,
                                      'new': "False",
                                      'old_name': edit_article.title})
        return render(request, 'create-article.html', {'form': form, 'is_new': False})
    elif action == "save-article" and request.method == 'POST' and request.user.is_authenticated:
        input_form = CreateArticle(request.POST, request.FILES)
        if input_form.is_valid():
            if input_form.cleaned_data['new'] == "True":
                article_instance = Article(
                    journal=Journal.objects.get(
                        journal_name=input_form.cleaned_data['journal'].replace("_", " ")),
                    author=UserProfile.objects.get(user=request.user),
                    title=input_form.cleaned_data['article_name'],
                    short_desc=input_form.cleaned_data['article_short_desk'],
                    body=input_form.cleaned_data['article_body'])
                article_instance.save()
            else:
                article_instance = Article.objects.get(
                    journal=Journal.objects.get(
                        journal_name=input_form.cleaned_data['journal'].replace("_", " ")),
                    author=UserProfile.objects.get(user=request.user),
                    title=input_form.cleaned_data['old_name'].replace("_", " ")
                )
                article_instance.title = input_form.cleaned_data['article_name']
                article_instance.short_desc = input_form.cleaned_data['article_short_desk']
                article_instance.body = input_form.cleaned_data['article_body']
                article_instance.save()
            return HttpResponseRedirect('/authors/' +
                                        request.user.username + '/journal/' +
                                        input_form.cleaned_data['journal'])
    elif action == "delete-article" and request.user.is_authenticated and journal_name != '':
        try:
            Article.objects.get(author=UserProfile.objects.get(user=request.user),
                                journal__journal_name=journal_name.replace("_", " "),
                                title=article_name.replace("_", " ")).delete()
        except exceptions.ObjectDoesNotExist:
            return HttpResponseBadRequest
        return HttpResponseRedirect('/authors/' + request.user.username + '/journal/' + journal_name)
    return HttpResponseBadRequest


# Shows articles in journal
def article(request, author_username, journal_name, article_name):
    article_instance = Article.objects.filter(journal=Journal.objects.
                                              get(journal_name=journal_name.replace("_", " "))). \
        get(title=article_name.replace("_", " "))
    content = {'article': article_instance,
               'author': author_username,
               'journal_name': journal_name,
               }
    return render(request, 'article.html', content)


# Shows user settings
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


# Save setup
def save_changes(request):
    if request.user.is_authenticated:
        user = UserProfile.objects.get(user__username=request.user)
        form = SettingsForm(request.POST, request.FILES)
        if form.is_valid():
            user.user.username = form.cleaned_data['username']
            if make_password(form.cleaned_data['old_password']) == user.user.password and \
                            form.cleaned_data['new_password'] != '':

                user.user.password = make_password(form.cleaned_data['new_password'])
            user.user.email = form.cleaned_data['email']
            user.save()
            user.short_describe = form.cleaned_data['describe_yourself']
            user.birth_year = form.cleaned_data['birth_year']
            user.gender = form.cleaned_data['gender']
            if form.cleaned_data['avatar'] is not None:
                user.avatar = form.cleaned_data['avatar']
            user.save()
            return HttpResponseRedirect('/authors/settings/')

    else:
        return render(request, 'login.html')


# Ajax subscribe
def ajax(request):
    # Subscribe function
    if request.POST.get('function') == 'subscribe':
        if request.user.is_authenticated and \
                UserProfile.objects.filter(user_id=request.POST.get('author')).exists() and \
                not UserProfile.objects.get(user=request.user).subscribed.filter(
                    id=request.POST.get('author')).exists():
            user = UserProfile.objects.get(user_id=request.user.id)
            user.subscribed.add(request.POST.get('author'))
            user.save()
            return HttpResponse("OK", status=200)
        return HttpResponse("User is not exists or already subscribed", status=200)
    # Unsubscribe function
    elif request.POST.get('function') == 'unsubscribe':
        if request.user.is_authenticated and \
                UserProfile.objects.filter(user_id=request.POST.get('author')).exists() and \
                UserProfile.objects.get(user=request.user).subscribed.filter(id=request.POST.get('author')).exists():
            user = UserProfile.objects.get(user_id=request.user.id)
            user.subscribed.remove(request.POST.get('author'))
            user.save()
            return HttpResponse("OK", status=200)
    return HttpResponse("Function is not familiar", status=404)

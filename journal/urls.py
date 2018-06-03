from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from journal import views

urlpatterns = [
    path('categories/', views.categories, name='categories'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    re_path(r'authors/$', views.authors, name='authors'),
    re_path(r'authors/(?P<author_username>\w+)/$', views.author, name='authors'),
    re_path(r'email-verification/(?P<email_key>\w+)/$', views.email_check, name='email_check'),
    path('email/', views.email_sighup, name='email_sighup'),
    path('', RedirectView.as_view(url='/categories/', permanent=True)),

]

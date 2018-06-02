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
    re_path(r'authors/$', views.authors, name='authors'),
    re_path(r'authors/(?P<author_username>\w+)/$', views.author, name='authors'),
    path('', RedirectView.as_view(url='/categories/', permanent=True)),

]

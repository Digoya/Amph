from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from journal import views

urlpatterns = [
    path('categories/', views.categories, name='categories'),
    path('authors/', views.authors, name='authors'),
    path('', views.categories),
]

from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('scrape', views.scraper, name='scraper'),
    path('crawler', views.crawler, name='crawler'),
    path('output', views.output, name='output'),
]

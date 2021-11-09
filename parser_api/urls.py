from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import GetDataView, HelpView


urlpatterns = [
    path('', GetDataView.as_view(), name='get_data_from_page'),
    path('help/', HelpView.as_view(), name='help'),
]

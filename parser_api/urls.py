from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'get_data_from_page', GetDataView, basename='get_data_from_page')

urlpatterns = [
    path('', include(routers.urls)),
]

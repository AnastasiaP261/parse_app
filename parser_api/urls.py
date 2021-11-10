from django.urls import path

from .views import GetDataView, HelpView

urlpatterns = [
    path('', GetDataView.as_view(), name='get_data_from_page'),
    path('help/', HelpView.as_view(), name='help'),
]

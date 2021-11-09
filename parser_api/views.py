from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from django.views import View
from django.http import HttpResponse


class GetDataView(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello world!')


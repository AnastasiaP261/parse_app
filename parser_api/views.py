from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

class GetDataView(viewsets.ViewSet):
    def list(self, request):
        return Responce

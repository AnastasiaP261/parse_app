from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from django.views import View
from django.http import HttpResponse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from .answers import *
import requests


DEFAULT_OUTPUT_TEXT_WIDTH = 110
DEFAULT_SAVING_IMG_LINKS = True


class GetDataView(View):
    params = {
        'url': '',
        'output_text_width': DEFAULT_OUTPUT_TEXT_WIDTH,
        'saving_img_links': DEFAULT_SAVING_IMG_LINKS,
    }

    def get(self, request, *args, **kwargs):
        if err := self.validation():
            return HttpResponse(err)

        return HttpResponse('Hello world!')

    def validation(self):
        if "url" not in self.request.GET:
            return HttpResponse(EMPTY_URL)
        else:
            r = requests.head(self.request.GET['url'])
            if r.status_code != 200:
                return INVALID_URL.format(r.status_code, r.reason)
            else:
                self.params['url'] = self.request.GET['url']

        if "output_text_width" in self.request.GET:
            try:
                if int(self.request.GET['output_text_width']) <= 0:
                    return INVALID_TEXT_WIDTH
                else:
                    self.params['output_text_width'] = int(self.request.GET['output_text_width'])
            except ValueError:
                return INVALID_TEXT_WIDTH


        if "saving_img_links" in self.request.GET:
            if self.request.GET['saving_img_links'] in ('False', 'false', '0'):
                self.params['saving_img_links'] = False
            elif self.request.GET['saving_img_links'] in ('True', 'true', '1'):
                self.params['saving_img_links'] = True
            else:
                return INVALID_IMG_LINKS

        return False


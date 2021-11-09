from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from .answers import *
import requests


DEFAULT_OUTPUT_TEXT_WIDTH = 110
DEFAULT_SAVING_IMG_LINKS = True


class GetDataView(TemplateView):
    params = {
        'url': '',
        'output_text_width': DEFAULT_OUTPUT_TEXT_WIDTH,
        'saving_img_links': DEFAULT_SAVING_IMG_LINKS,
    }

    def get(self, request, *args, **kwargs):
        if answ := self.validation():
            return render(request, 'error.html', {'err': answ})

        return HttpResponse('Hello world!')

    def validation(self):
        # валидация url
        if "url" not in self.request.GET:
            return {'text': EMPTY_URL, }
        else:
            r = requests.head(self.request.GET['url'])
            if r.status_code != 200:
                return {'text': INVALID_URL, 'code': r.status_code, 'reason': r.reason}
            else:
                self.params['url'] = self.request.GET['url']

        # валидация ширины текста
        if "output_text_width" in self.request.GET:
            try:
                if int(self.request.GET['output_text_width']) <= 0:
                    return {'text': INVALID_TEXT_WIDTH, }
                else:
                    self.params['output_text_width'] = int(self.request.GET['output_text_width'])
            except ValueError:
                return {'text': INVALID_TEXT_WIDTH, }

        # валидация параметра отвечающего за сохранение ссылок
        if "saving_img_links" in self.request.GET:
            if self.request.GET['saving_img_links'] in ('False', 'false', '0'):
                self.params['saving_img_links'] = False
            elif self.request.GET['saving_img_links'] in ('True', 'true', '1'):
                self.params['saving_img_links'] = True
            else:
                return {'text': INVALID_IMG_LINKS, }

        return False


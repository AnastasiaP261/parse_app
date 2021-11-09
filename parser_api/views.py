import re

import requests
from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from .answers import *

DEFAULT_OUTPUT_TEXT_WIDTH = 110
DEFAULT_SAVING_IMG_LINKS = True
VIEW_TAGS = ('h1', 'p', 'ul', 'ol', 'li')
NOT_VIEW_TAGS = ('footer', 'header')


class GetDataView(TemplateView):
    params = {
        'url': '',
        'output_text_width': DEFAULT_OUTPUT_TEXT_WIDTH,
        'saving_img_links': DEFAULT_SAVING_IMG_LINKS,
    }

    def get(self, request, *args, **kwargs):
        if answ := self.validation():
            return render(request, 'error.html', {'err': answ})

        text = self.parse_url()

        resp = HttpResponse(text, content_type='text/plain')
        resp['Content-Disposition'] = 'attachment; filename={}.txt'.format('answer')
        return resp

    def parse_url(self):
        parse_site = requests.get(self.params['url'])
        soup = BeautifulSoup(parse_site.text, 'html.parser')

        content = ''
        for div in soup.body:
            if div.name in ('div', 'main') and not self.seach_header_footer(div.attrs):
                for child in div.recursiveChildGenerator():
                    if child.name in VIEW_TAGS:
                        content += child.text + '\n'
                    elif self.params['saving_img_links'] and child.name == 'img':
                        content += f'IMAGE({child.attrs["src"]})\n'

        return content.strip()

    @staticmethod
    def seach_header_footer(attrs):
        if 'class' in attrs:
            for cl in attrs['class']:
                cl = cl.lower()
                if cl.find('footer') != -1 or cl.find('header') != -1:
                    return True

        if 'id' in attrs:
            cl = attrs['id'].lower()
            if cl.find('footer') != -1 or cl.find('header') != -1:
                return True

        return False

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


class HelpView(TemplateView):
    template_name = 'help.html'

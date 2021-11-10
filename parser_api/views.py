import re
import textwrap as tw

import requests
from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from .answers import *

DEFAULT_OUTPUT_TEXT_WIDTH = 110
DEFAULT_SAVING_IMG_LINKS = True
FILE_NAME = 'answer'
VIEW_TAGS = ('h1', 'h2', 'h3', 'p', 'ul', 'ol', 'li')
NOT_VIEW_TAGS = ('footer', 'header')


class GetDataView(TemplateView):
    params = {
        'url': '',  # url сайта который будет парситься
        'output_text_width': DEFAULT_OUTPUT_TEXT_WIDTH,  # ширина выходного файла в символах
        'saving_img_links': DEFAULT_SAVING_IMG_LINKS,  # нужно ли добавлять ссылки на картинки
        'file_name': FILE_NAME,  # возможность поменять имя выходного файла
    }

    def get(self, request, *args, **kwargs):
        if answ := self.validation():
            return render(request, 'error.html', {'err': answ})

        text = self.parse_url()

        resp = HttpResponse(text, content_type='text/plain')
        resp['Content-Disposition'] = f'attachment; filename={self.params["file_name"]}.txt'
        return resp

    def parse_url(self):
        parse_site = requests.get(self.params['url'])
        soup = BeautifulSoup(parse_site.text, 'html.parser')

        content = ''
        for div in soup.body:
            # в body нам необходимы только теги div и main(тк иногда встречаются еще теги header и footer)
            # еще определить футер или хедер можно по названиям классов или ид тегов

            if div.name in ('div', 'main') and not self.search_header_footer(div.attrs):
                for child in div.recursiveChildGenerator():  # от каждого найденного тега строим дерево

                    if child.name in VIEW_TAGS:  # проверка контента на "полезность"
                        # wrap используется для разбиения абзаца на строки указанной ширины
                        content += '\n'.join(tw.wrap(
                            child.text, width=self.params['output_text_width']
                        )) + '\n\n'

                    elif self.params['saving_img_links'] and child.name == 'img':  # есди надо, добавляются изображения
                        content += '\n'.join(tw.wrap(
                            f'IMAGE({child.attrs["src"]})', width=self.params['output_text_width']
                        )) + '\n\n'

        return content.strip()

    @staticmethod
    def search_header_footer(attrs):
        # чекаем классы и ид тега, чтобы понять, является ли он основным контентом или это одна из шапок сайта
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
        if answ := self.valid_url():
            return answ

        # валидация ширины текста
        if answ := self.valid_output_text_width():
            return answ

        # валидация параметра отвечающего за сохранение ссылок
        if answ := self.valid_saving_img_links():
            return answ

        # валидация имени выходного файла
        if answ := self.valid_file_name():
            return answ

        return False

    def valid_url(self):
        if "url" not in self.request.GET:
            return EMPTY_URL
        else:
            r = requests.head(self.request.GET['url'])
            if r.status_code != 200:
                return {
                    'text': INVALID_URL['text'],
                    'reason': INVALID_URL['reason'].format(r.status_code, r.reason),
                }
            else:
                self.params['url'] = self.request.GET['url']
        return False

    def valid_output_text_width(self):
        if "output_text_width" in self.request.GET:
            try:
                if int(self.request.GET['output_text_width']) <= 0:
                    return INVALID_TEXT_WIDTH
                else:
                    self.params['output_text_width'] = int(self.request.GET['output_text_width'])
            except ValueError:
                return INVALID_TEXT_WIDTH
        return False

    def valid_saving_img_links(self):
        if "saving_img_links" in self.request.GET:
            if self.request.GET['saving_img_links'] in ('False', 'false', '0'):
                self.params['saving_img_links'] = False
            elif self.request.GET['saving_img_links'] in ('True', 'true', '1'):
                self.params['saving_img_links'] = True
            else:
                return INVALID_IMG_LINKS
        return False

    def valid_file_name(self):
        if 'file_name' in self.request.GET:
            if re.search(r'^[\w\-]+$', self.request.GET['file_name']):
                self.params['file_name'] = self.request.GET['file_name']
            else:
                return INVALID_FILE_NAME
        return False


class HelpView(TemplateView):
    template_name = 'help.html'

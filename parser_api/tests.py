from django.test import TestCase, Client
from django.urls import reverse

from .answers import *


class HelpReqTestCase(TestCase):

    def test_request_ok(self):
        cl = Client()
        r = cl.get(reverse('help'))
        self.assertEqual(r.status_code, 200)
        self.assertTemplateUsed('help.html')


class GetDataTestCase(TestCase):
    url = 'http://127.0.0.1:8000/parse/'
    url_for_parse = 'https://docs.python.org/3.8/'

    def test_valid_request(self):
        cl = Client()
        r = cl.get(
            path=self.url,
            data={
                'url': self.url_for_parse
            },
        )
        self.assertEqual(r.status_code, 200)
        self.assertTemplateNotUsed('error.html')

    def test_invalid_url(self):
        cl = Client()
        r = cl.get(
            path=self.url,
            data={
                'url': self.url_for_parse + 'invalid_invalid/'
            },
        )
        self.assertEqual(r.status_code, 200)
        self.assertTemplateUsed('error.html')
        self.assertInHTML('<p>404 Not Found - URL Is Invalid</p>', str(r.content))

    def test_empty_url(self):
        cl = Client()
        r = cl.get(
            path=self.url,
            data={},
        )
        self.assertEqual(r.status_code, 200)
        self.assertTemplateUsed('error.html')
        self.assertInHTML(f'<p>{EMPTY_URL["reason"]}</p>', str(r.content))

    def test_output_text_width(self):
        def get_resp():
            cl = Client()
            r = cl.get(
                path=self.url,
                data={
                    'url': self.url_for_parse,
                    'output_text_width': n,
                },
            )
            return r

        # не валидные кейсы
        for n in (0, -1, 200.2):
            resp = get_resp()
            self.assertEqual(resp.status_code, 200)
            self.assertTemplateUsed('error.html')
            self.assertInHTML(f'<p>{INVALID_TEXT_WIDTH["reason"]}</p>', str(resp.content))

        # валидные кейсы
        for n in (1, 210, 33000):
            resp = get_resp()
            self.assertEqual(resp.status_code, 200)
            self.assertTemplateNotUsed('error.html')

    def test_saving_img_links(self):
        def get_resp():
            cl = Client()
            r = cl.get(
                path=self.url,
                data={
                    'url': self.url_for_parse,
                    'saving_img_links': n,
                },
            )
            return r

        # не валидные кейсы
        for n in (-1, 'TRUE', 'string', '-1', ''):
            resp = get_resp()
            self.assertEqual(resp.status_code, 200)
            self.assertTemplateUsed('error.html')
            self.assertInHTML(f'<p>{INVALID_IMG_LINKS["reason"]}</p>', str(resp.content))

        # валидные кейсы
        for n in (1, 0, 'True', 'False', 'true', 'false', True, False, '0', '1'):
            resp = get_resp()
            self.assertEqual(resp.status_code, 200)
            self.assertTemplateNotUsed('error.html')

    def test_file_name(self):
        def get_resp():
            cl = Client()
            r = cl.get(
                path=self.url,
                data={
                    'url': self.url_for_parse,
                    'file_name': n,
                },
            )
            return r

        # не валидные кейсы
        for n in ('', 'text.txt', 'Text+'):
            resp = get_resp()
            self.assertEqual(resp.status_code, 200)
            self.assertTemplateUsed('error.html')
            self.assertInHTML(f'<p>{INVALID_FILE_NAME["reason"]}</p>', str(resp.content))

        # валидные кейсы
        for n in ('text', 'TEXT', 'TexT123_Текст-123', 't'):
            resp = get_resp()
            self.assertEqual(resp.status_code, 200)
            self.assertTemplateNotUsed('error.html')

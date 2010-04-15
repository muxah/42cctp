import datetime
import django
from django.test import TestCase
from django.test.client import Client

from models import BusinessCard


BCARD_FIELDS = ('first_name', 'last_name', 'email', 'description', 'birth_date',)
CREDENTIALS = {'username': 'mynameisMike', 'password': 'letmein',}
PROTECTED_PAGES_URLS = ('/', '/edit/',)


class TemlateContextProcessorsTest(TestCase):

    def test_existence_and_format(self):
        from bcard.context_processors import settings
        result = settings('dummy')
        self.assertTrue(isinstance(result, dict))
        self.assertRaises(TypeError, settings)

    def test_integration(self):
        from settings import TEMPLATE_CONTEXT_PROCESSORS
        cpf = 'bcard.context_processors.settings'
        self.assertTrue(cpf in TEMPLATE_CONTEXT_PROCESSORS)


class EditBCFormTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.client.login(**CREDENTIALS)
        self.url = '/edit/'

    def tearDown(self):
        self.client.logout()

    def test_form_existence_and_format(self):
        from bcard.forms import EditBusinessCardForm as EBCF
        cls = django.forms.models.ModelFormMetaclass
        self.assertTrue(isinstance(EBCF, cls))
        fields = [f.name for f in EBCF().visible_fields()]

        for a in BCARD_FIELDS:
            self.assertTrue(a in fields)

        for i in range(len(fields)):
            self.assertEqual(fields[i], BCARD_FIELDS[::-1][i])

    def test_form_integration(self):
        from views import EditBusinessCardForm

    def test_view_existance_and_format(self):
        from views import edit

        self.assertRaises(TypeError, edit)
        response = self.client.get(self.url)
        response.context['form']

        ids = ['id_%s' % a for a in BCARD_FIELDS]
        for id in ids:
            self.assertTrue(id in response.content)

        self.assertTrue('method="post"' in response.content)

    def test_view_integration(self):
        from urls import edit

        response = self.client.get(self.url)
        self.failUnlessEqual(response.status_code, 200)
        person = BusinessCard.objects.get(pk=1)

        for a in BCARD_FIELDS:
            self.assertTrue(str(getattr(person, a)) in response.content)

    def test_functionality(self):
        required = {'first_name': 'Mate', 'last_name': 'Rolling'}
        required['birth_date'] = datetime.date(1999, 10, 20)
        optional = {'email': 'mate@rolling.com', 'description': 'Nothing to c.'}
        all = required
        all.update(optional)
        empty = dict([(k, '') for k in BCARD_FIELDS])
        incorrect = all.copy()
        incorrect['email'] = 'broken_email'
        ajax_attrs = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}

        for d in (empty, optional, incorrect):
            r = self.client.post(self.url, d)
            ajax_r = self.client.post(self.url, d, **ajax_attrs)

            for response in (r, ajax_r):
                self.assertEqual(response.status_code, 200)
                self.assertTrue('class="error"' in response.content)
                self.assertTrue("name='csrfmiddlewaretoken'" in response.content)
                self.assertTrue('edit.html' in [t.name for t in response.template])

        for d in (required, all):
            r = self.client.post(self.url, d, follow=True)
            ajax_r = self.client.post(self.url, d, **ajax_attrs)

            for response in (ajax_r, r):
                self.assertEqual(response.status_code, 200)
                person = BusinessCard.objects.get(pk=1)

                for k, v in d.items():
                     self.assertEqual(unicode(v), unicode(getattr(person, k)))

            self.assertTrue(('http://testserver/', 302) in response.redirect_chain)
            self.assertTrue('home.html' in [t.name for t in response.template])


class CSSTest(TestCase):

    def test_integration(self):
        from urls import settings as S
        from settings import MEDIA_URL as MU
        from settings import MEDIA_ROOT as MR

        self.assertTrue(MU)
        self.assertTrue(MR)


class AuthTest(TestCase):

    def setUp(self):
        from settings import LOGIN_REDIRECT_URL as LRU
        from settings import LOGIN_URL as LU
        self.client = Client()
        self.login_url = LU
        self.template = 'login.html'
        self.landing_url = LRU
        self.logout_url = '/logout/'
        self.intruder = {'username': 'evil', 'password': 'someone',}

    def test_integration(self):
        from views import login_required
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)

    def test_login_page_existence(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.template in [t.name for t in response.template])

        elements = ('<!DOCTYPE html', 'id_password', 'id_username', 'type="submit"')
        for e in elements:
            self.assertTrue(e in response.content)

    def test_logging_in(self):
        for d in (self.intruder, CREDENTIALS):
            response = self.client.post(self.login_url, d, follow=True)
            self.assertEqual(response.status_code, 200)

        self.assertTrue(('http://testserver/', 302) in response.redirect_chain)

    def test_pages_protection(self):
        redirect_url = 'http://testserver' + self.login_url + '?next=%s'
        for url in PROTECTED_PAGES_URLS:
            response = self.client.get(url, follow=True)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(self.template in [t.name for t in response.template])
            self.assertTrue((redirect_url % url, 302) in response.redirect_chain)

    def test_log_out_page(self):
        destination = 'http://testserver' + self.login_url
        response = self.client.get(self.logout_url, follow=True)
        self.assertTrue((destination, 302) in response.redirect_chain)
        self.assertTrue(self.template in [t.name for t in response.template])

    def test_logout_link_existence(self):
        link = 'href="%s"' % self.logout_url
        self.client.login(**CREDENTIALS)

        for url in PROTECTED_PAGES_URLS:
            response = self.client.get(url)
            self.assertTrue(link in response.content)

        response = self.client.get(self.login_url)
        self.assertFalse(link in response.content)


class HomePageTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_existence(self):
        from bcard.views import home
        from settings import TEMPLATE_DIRS as TD

        self.assertRaises(TypeError, home)
        self.assertTrue(TD)

    def test_content(self):
        self.client.login(**CREDENTIALS)
        response = self.client.get('/')
        self.client.logout()
        self.assertEqual(response.status_code, 200)
        self.assertTrue('<!DOCTYPE html' in response.content)
        self.assertTrue('home.html' in [t.name for t in response.template])

        from models import BusinessCard as BC
        bc = BC.objects.get(pk=1)

        for f in BCARD_FIELDS:
            self.assertTrue(str(getattr(bc, f)) in response.content)


class TemplateTagTest(TestCase):

    def test_integration_and_existence(self):
        from templatetags.bcard_extra import register
        self.assertTrue('edit_list' in register.tags.keys())

    def test_functionality(self):
        from bcard.templatetags.bcard_extra import edit_list
        from django.contrib.auth.models import User
        obj = User.objects.get(pk=2)
        self.assertEqual(edit_list(obj), '/admin/auth/user/2/')


class CommandTest(TestCase):

    def test_existence_and_format(self):
        from django.core.management.base import BaseCommand
        from management.commands.list import Command
        import os

        self.assertTrue(hasattr(Command, 'help'))
        self.assertTrue(hasattr(Command, 'handle'))
        self.assertEqual(Command.__base__, BaseCommand)
        os.system('python manage.py list')

from django.test import TestCase
from django.test.client import Client
import django

from models import BusinessCard

BCARD_FIELDS = ('first_name', 'last_name', 'email', 'description',)


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

    def test_existence_and_format(self):
        from bcard.forms import EditBusinessCardForm
        cls = django.forms.models.ModelFormMetaclass
        self.assertTrue(isinstance(EditBusinessCardForm, cls))
        fields = [f.name for f in EditBusinessCardForm().visible_fields()]

        for a in BCARD_FIELDS:
            self.assertTrue(a in fields)

    def test_integration(self):
        from views import EditBusinessCardForm


class EditBCViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = '/edit/'

    def test_existance_and_format(self):
        from views import edit

        self.assertRaises(TypeError, edit)
        response = self.client.get(self.url)
        response.context['form']

        ids = ['id_%s' % a for a in BCARD_FIELDS]
        for id in ids:
            self.assertTrue(id in response.content)

        self.assertTrue('method="post"' in response.content)

    def test_integration(self):
        from urls import edit

        response = self.client.get(self.url)
        self.failUnlessEqual(response.status_code, 200)
        person = BusinessCard.objects.get(pk=1)
        for a in BCARD_FIELDS:
            self.assertTrue(getattr(person, a) in response.content)

    def test_functionality(self):
        required = {'first_name': 'Mate', 'last_name': 'Rolling'}
        optional = {'email': 'mate@rolling.com', 'description': 'Nothing to c.'}
        all = required
        all.update(optional)
        empty = dict([(k, '') for k in BCARD_FIELDS])
        incorrect = all.copy()
        incorrect['email'] = 'broken_email'
        default = {}

        for d in (empty, optional, incorrect):
            response = self.client.post(self.url, d)
            self.assertEqual(response.status_code, 200)
            self.assertTrue('class="errorlist"' in response.content)
            self.assertTrue("name='csrfmiddlewaretoken'" in response.content)
            self.assertTrue('edit.html' in [t.name for t in response.template])

        for d in (default, required, all):
            response = self.client.post(self.url, all, follow=True)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(('http://testserver/', 302) in response.redirect_chain)
            self.assertTrue('home.html' in [t.name for t in response.template])

            person = BusinessCard.objects.get(pk=1)
            for k, v in d.items():
                 self.assertEqual(unicode(v), getattr(person, k))


__test__ = {"doctest": """
>>> from bcard.views import home
>>> home()
Traceback (most recent call last):
...
TypeError: home() takes exactly 1 ...

>>> type(home('1'))
<class 'django.http.HttpResponse'>

>>> from settings import TEMPLATE_DIRS
>>> bool(TEMPLATE_DIRS)
True

>>> from django.test.client import Client
>>> c = Client()
>>> response = c.get('/')
>>> response.status_code
200

>>> rc = response.content
>>> rc
'<!DOCTYPE html...'

>>> from models import BusinessCard as BC
>>> bc = BC.objects.get(pk=1)
>>> bc.first_name in rc
True
>>> bc.last_name in rc
True
>>> bc.email in rc
True
>>> bc.description in rc
True

"""}

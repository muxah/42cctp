from django.test import TestCase


class TemlateContextProcessorsTest(TestCase):

    def test_existence_and_format(self):
        try:
            from bcard.context_processors import settings
        except ImportError as e:
            self.fail(e)
        else:
            result = settings('dummy')
            self.assertTrue(isinstance(result, dict))
            self.assertRaises(TypeError, settings)

    def test_integration(self):
        try:
            from settings import TEMPLATE_CONTEXT_PROCESSORS
        except ImportError as e:
            self.fail(e)
        else:
            cpf = 'bcard.context_processors.settings'
            self.assertTrue(cpf in TEMPLATE_CONTEXT_PROCESSORS)


class EditBCFormTest(TestCase):

    def test_existence_and_format(self):
        try:
            from bcard.forms import EditBusinessCardForm
        except ImportError as e:
            self.fail(e)
        else:
            import django
            cls = django.forms.models.ModelFormMetaclass
            self.assertTrue(isinstance(EditBusinessCardForm, cls))

            for a in ('first_name', 'last_name', 'email', 'description',):
                self.assertTrue(hasattr(EditBusinessCardForm, a))

    def test_integration(self):
        try:
            from views import EditBusinessCardForm
        except ImportError as e:
            self.fail(e)


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

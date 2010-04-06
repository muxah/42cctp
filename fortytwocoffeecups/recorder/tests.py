from django.test import TestCase
from django.test.client import Client
from models import RecordedRequest

class RequestIsStoredTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.d = {'one': 1, 'two': 2}
        self.expected = "%s:<QueryDict: {u'two': [u'2'], u'one': [u'1']}"

    def test_get_is_stored(self):
        self.client.get('/', self.d)
        request = RecordedRequest.objects.latest('pk').request
        e = self.expected % 'GET'
        self.failUnless(e in request)


    def test_post_is_stored(self):
        self.client.post('/', self.d)
        request = RecordedRequest.objects.latest('pk').request
        e = self.expected % 'POST'
        self.failUnless(e in request)


__test__ = {"doctest": """
>>> from recorder.middleware import RecordingMiddleware as RM
>>> hasattr(RM, 'process_request')
True

>>> RM.process_request()
Traceback (most recent call last):
...
TypeError: unbound method process_request() must be called with ...

>>> RM().process_request()
Traceback (most recent call last):
...
TypeError: process_request() takes exactly 2 ...

>>> RM().process_request('dummy request')

>>> from settings import MIDDLEWARE_CLASSES as MC
>>> 'recorder.middleware.RecordingMiddleware' in MC
True

>>> from models import RecordedRequest as RR
"""}
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

    def test_existence_and_format(self):
        from recorder.middleware import RecordingMiddleware as RM
        self.assertTrue(hasattr(RM, 'process_request'))
        self.assertRaises(TypeError, RM.edit)
        self.assertRaises(TypeError, RM().edit)

    def test_integration(self):
        from models import RecordedRequest
        from settings import MIDDLEWARE_CLASSES as MC
        self.assertTrue('recorder.middleware.RecordingMiddleware' in MC)

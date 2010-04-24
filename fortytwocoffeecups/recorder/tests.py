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
        self.assertRaises(TypeError, RM.process_request)
        self.assertRaises(TypeError, RM().process_request)

    def test_integration(self):
        from models import RecordedRequest
        from settings import MIDDLEWARE_CLASSES as MC
        self.assertTrue('recorder.middleware.RecordingMiddleware' in MC)


class SignalIsStoredTest(TestCase):

    def test_init_is_stored(self):
        from models import RecordedRequest as RR
        from models import RecordedSignal as RS

        before_init = RS.objects.count()
        obj = RR(request=repr({'dummy': 'request'}))
        after_init = RS.objects.count()
        obj.save()
        after_save = RS.objects.count()
        obj.delete()
        after_delete = RS.objects.count()

        self.assertEqual(after_init - before_init, 1)
        self.assertEqual(after_save - after_init, 1)
        self.assertEqual(after_delete - after_save, 1)

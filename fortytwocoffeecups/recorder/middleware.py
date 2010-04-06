from models import RecordedRequest


class RecordingMiddleware(object):

    def process_request(self, request):
        rr = RecordedRequest(request=repr(request))
        rr.save()

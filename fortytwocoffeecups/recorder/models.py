from django.db import models


class RecordedRequest(models.Model):
    """
    Model purposed for storing each http request by RecordingMiddleware.

    # It is possible to store new request:
    >>> dummy_request = {'dummy':'request'}
    >>> rr = RecordedRequest(request=repr(dummy_request))
    >>> rr.save()

    """

    request = models.TextField(max_length=10000)

from django.db import models

from django.db.models.signals import post_init
from django.db.models.signals import post_save
from django.db.models.signals import post_delete


class RecordedRequest(models.Model):
    """
    Model purposed for storing each http request by RecordingMiddleware.

    # It is possible to store new request:
    >>> dummy_request = {'dummy':'request'}
    >>> rr = RecordedRequest(request=repr(dummy_request))
    >>> rr.save()

    """

    request = models.TextField(max_length=10000)


class RecordedSignal(models.Model):
    """
    Model pusposed for storing each post- init/save/delete signal
    for each project model.

    >>> rs = RecordedSignal(sender='sender model', kwargs="{'dummy': 'args'}")
    >>> rs.save()

    """

    sender = models.CharField(max_length=100)
    kwargs = models.TextField(max_length=1000)


def store_signals(sender, **kwargs):
    if sender != RecordedSignal:
        RecordedSignal(sender=str(sender), kwargs=repr(kwargs)).save()


post_init.connect(store_signals)
post_save.connect(store_signals)
post_delete.connect(store_signals)

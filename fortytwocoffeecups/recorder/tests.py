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

"""}

from django import conf


def settings(request):
    return {'settings': conf.settings}

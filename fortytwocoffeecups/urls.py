from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

from bcard.views import home
from bcard.views import edit


urlpatterns = patterns('',
    (r'^$', home),
    url(r'^edit/$', edit, {'template': 'edit.html'}, name='edit'),
    (r'^edit/form/$', edit, {'template': 'form.html'}),
    (r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'login.html'}),
    (r'^logout/$', 'django.contrib.auth.views.logout_then_login'),
    (r'^outthebox/jsi18n', 'django.views.i18n.javascript_catalog'),
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^%s(.*)' % settings.MEDIA_URL, 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
)

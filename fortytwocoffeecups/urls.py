from django.conf.urls.defaults import *
from django.conf import settings

from bcard.views import home
from bcard.views import edit


urlpatterns = patterns('',
    (r'^$', home),
    (r'^edit/$', edit),
    # Example:
    # (r'^fortytwocoffeecups/', include('fortytwocoffeecups.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^%s(.*)' % settings.MEDIA_URL, 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
)

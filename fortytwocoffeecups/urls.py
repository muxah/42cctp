from django.conf.urls.defaults import *

from bcard.views import home


urlpatterns = patterns('',
    (r'^$', home),
    # Example:
    # (r'^fortytwocoffeecups/', include('fortytwocoffeecups.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)

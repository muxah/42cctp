from django import template
from django.core.urlresolvers import reverse

register = template.Library()


def edit_list(obj):
    from django.contrib.contenttypes.models import ContentType
    ct = ContentType.objects.get_for_model(obj)
    url = 'admin:%s_%s_change' % (ct.app_label, ct.model)
    return reverse(url, args=(str(obj.id),))

register.simple_tag(edit_list)

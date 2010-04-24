from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import login_required

from models import BusinessCard
from forms import EditBusinessCardForm


@login_required
def home(request):
    try:
        person = BusinessCard.objects.get(pk=1)
    except DoesNotExist:
        person = None

    return render_to_response('home.html', {'person': person})


@login_required
def edit(request, template):
    person = BusinessCard.objects.get(pk=1)
    form = EditBusinessCardForm(instance=person)

    if request.method == 'POST':
        form = EditBusinessCardForm(request.POST)

        if form.is_valid():
            for a in form.base_fields.keys():
                v = form.cleaned_data.get(a, None)
                if v is not None:
                    setattr(person, a, v)
            person.save()

            if not request.is_ajax():
                return HttpResponseRedirect('/')

    return render_to_response(template,
                             {'form': form},
                             context_instance=RequestContext(request))

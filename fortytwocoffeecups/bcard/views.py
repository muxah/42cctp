from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect

from models import BusinessCard
from forms import EditBusinessCardForm


def home(request):
    try:
        person = BusinessCard.objects.get(pk=1)
    except DoesNotExist:
        person = None

    return render_to_response('home.html', {'person': person,})


def edit(request):
    person = BusinessCard.objects.get(pk=1)
    form = EditBusinessCardForm(instance=person)

    if request.method == 'POST':
        form = EditBusinessCardForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/')

    return render_to_response('edit.html',
                             {'form': form},
                             context_instance=RequestContext(request))

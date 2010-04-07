from django.shortcuts import render_to_response
from models import BusinessCard
from forms import EditBusinessCardForm


def home(request):
    try:
        person = BusinessCard.objects.get(pk=1)
    except DoesNotExist:
        person = None

    return render_to_response('home.html', {'person': person,})


def edit(request):
    return render_to_response('edit.html', {})

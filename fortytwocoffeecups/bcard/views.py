from django.shortcuts import render_to_response
from models import BusinessCard

def home(request):
    try:
        person = BusinessCard.objects.get(pk=1)
    except DoesNotExist:
        person = None

    return render_to_response('home.html', {'person': person,})

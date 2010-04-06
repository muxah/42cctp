from django.db import models


class BusinessCard(models.Model):
    """
    Model replicating business card function:
    storing card owner's name, description and contact information.

    # There should be an initial data set already:
    >>> initial = BusinessCard.objects.get(pk=1)

    # Only one though:
    >>> second = BusinessCard.objects.get(pk=2)
    ...
    DoesNotExist: ...

    # It is possible to add new bcard.
    >>> info = {first_name: 'Dude', last_name: 'Awesomer',}
    >>> bc = BusinessCard.objects.create(**info)

    # And fullfill it with the rest information and get it back:
    >>> bc.email = 'dude@awesomer.info'
    >>> bc.description = 'Some stuff about me goes here.'
    >>> bc.save()
    >>> bc.email
    'dude@awesomer.info'
    >>> bd.description
    'Some stuff about me goes here.'
    >>> bc.first_name
    'Dude'
    >>> bc.last_name
    'Awesomer'

    """

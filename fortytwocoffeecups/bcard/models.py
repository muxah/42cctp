from django.db import models


class BusinessCard(models.Model):
    """
    Model replicating business card function:
    storing card owner's name, description and contact information.

    # There should be an initial data set already:
    >>> initial = BusinessCard.objects.get(pk=1)

    # Only one though:
    >>> second = BusinessCard.objects.get(pk=2)
    Traceback (most recent call last):
        ...
    DoesNotExist: ...

    # It is possible to add new bcard.
    >>> bc = BusinessCard(first_name='Dude', last_name='Awesomer')
    >>> bc.save()

    # And fullfill it with the rest information and get it back:
    >>> bc.email = 'dude@awesomer.info'
    >>> bc.description = 'Some stuff about me goes here.'
    >>> bc.birth_date = '1986-08-20'
    >>> bc.save()
    >>> bc.email
    'dude@awesomer.info'
    >>> bc.description
    'Some stuff about me goes here.'
    >>> bc.first_name
    'Dude'
    >>> bc.last_name
    'Awesomer'

    """

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, blank=True)
    email = models.EmailField(blank=True)
    birth_date = models.DateField(blank=True, null=True)

from django import forms
from models import BusinessCard
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.admin.widgets import AdminDateWidget

class EditBusinessCardForm(forms.ModelForm):
    birth_date = forms.DateField(widget=AdminDateWidget)

    class Meta:
        model = BusinessCard
        fields = ('first_name', 'last_name', 'email', 'description', 'birth_date',)
        fields = fields[::-1]

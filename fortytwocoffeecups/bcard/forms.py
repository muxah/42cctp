from django import forms
from models import BusinessCard

class EditBusinessCardForm(forms.ModelForm):
    class Meta:
        model = BusinessCard

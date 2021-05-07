from django import forms
from .models import Enrolment

class SaveProfiles(forms.Form):
    profile = forms.NumberInput()
    drets_imatge = forms.BooleanField()
    salides_excursio = forms.BooleanField()
    salides_extra = forms.BooleanField()
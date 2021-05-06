""" from django import forms
from .models import MP

class PostForm(forms.ModelForm):

    class Meta:
        model = MP
        fields = ('name', 'code') """
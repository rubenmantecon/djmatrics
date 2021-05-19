from django import forms
from .models import Enrolment

class SaveProfiles(forms.Form):
    profile = forms.NumberInput()
    drets_imatge = forms.BooleanField()
    salides_excursio = forms.BooleanField()
    salides_extra = forms.BooleanField()


class ReviewForm(forms.Form):
    name = forms.CharField(
        label='Firstname', max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Firstname', 'id': 'form-firstname'}
        ))
    email = forms.EmailField(
        max_length=200, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'form-email'}
        ))
    review = forms.CharField(
        label='Review', widget=forms.Textarea(
            attrs={'class': 'form-control',  'id': 'form-review'}
        ))
    def send_mail(self):
        send_review_email.task.delay(
        self.claened_data['name'], self.cleaned_data['email'], self.cleaned_data['review'])
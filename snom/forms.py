from django import forms
from snom.models import Phone, FunctionKeys
from django.db import models


class FKeys(forms.Form):
    def __init__(self, *args, **kwargs):
        choices = kwargs.pop("choices")
        super(FKeys, self).__init__(*args, **kwargs)
        self.fields['user'].choices = choices

    #phones = forms.ModelChoiceField(queryset=Phone.objects.all())
    user = forms.ChoiceField(choices=())

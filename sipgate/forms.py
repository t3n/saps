from django import forms

from snom.models import Phone


class AssignForm(forms.Form):
    def __init__(self, *args, **kwargs):
        choices = kwargs.pop("choices")
        super(AssignForm, self).__init__(*args, **kwargs)
        self.fields['user'].choices = choices

    phones = forms.ModelChoiceField(queryset=Phone.objects.all())
    user = forms.ChoiceField(choices=())

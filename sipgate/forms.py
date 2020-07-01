from django import forms

from snom.models import Phone


class AssignForm(forms.Form):
    def __init__(self, *args, **kwargs):
        choices = kwargs.pop("choices")
        super(AssignForm, self).__init__(*args, **kwargs)
        self.fields["user"].choices = choices

        if "device" in self.data:
            self.fields["device"].choices = [(self.data["device"], "")]

    phone = forms.ModelChoiceField(queryset=Phone.objects.all())
    user = forms.ChoiceField(choices=())
    device = forms.ChoiceField()

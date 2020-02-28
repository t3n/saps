from django import forms

class ContactForm(forms.Form):
    def __init__(self, *args, **kwargs):
        choices = kwargs.pop("choices")
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['user'].choices = choices

    user = forms.ChoiceField(choices=())

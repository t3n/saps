from django import forms
MY_CHOICES = (
    ('1', 'Option 1'),
    ('2', 'Option 2'),
    ('3', 'Option 3'),
)

class ContactForm(forms.Form):
    def __init__(self, phone_choices, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['phone'].choices = phone_choices
        print(phone_choices)

    phone = forms.ChoiceField(choices=())


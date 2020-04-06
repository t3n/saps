from django import forms


class FunctionKeyForm(forms.Form):
    def __init__(self, *args, **kwargs):
        fkeys = kwargs.pop('fkeys')
        super(FunctionKeyForm, self).__init__(*args, **kwargs)

        for i, fkey in enumerate(fkeys):
            self.fields['fkey_%s' % i] = forms.CharField(label=fkey.fkey, initial=fkey.function, required=False)

    def function_keys(self):
        for name, value in self.cleaned_data.items():
            if name.startswith('fkey_'):
                yield (self.fields[name].label, value)

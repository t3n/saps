from django import forms

from .models import KIND_CHOICES


class FunctionKeyForm(forms.Form):
    def __init__(self, *args, **kwargs):
        fkeys = kwargs.pop("fkeys")
        super(FunctionKeyForm, self).__init__(*args, **kwargs)

        for i, fkey in enumerate(fkeys):
            self.fields["fkey_%s_kind" % i] = forms.ChoiceField(
                choices=[("", "")] + KIND_CHOICES,
                label=fkey.fkey,
                initial=fkey.kind,
                required=False,
            )
            self.fields["fkey_%s_kind" % i].widget.attrs.update(
                {"input type": "text", "class": "form-control"}
            )
            self.fields["fkey_%s_number" % i] = forms.CharField(
                label="", initial=fkey.number, required=False
            )
            self.fields["fkey_%s_number" % i].widget.attrs.update(
                {"input type": "text", "class": "form-control"}
            )

    def function_keys(self):
        for oname, ovalue in self.cleaned_data.items():
            if self.fields[oname].label:
                for iname, ivalue in self.cleaned_data.items():
                    if (
                        not self.fields[iname].label
                        and oname.split("_")[1] == iname.split("_")[1]
                    ):
                        yield (self.fields[oname].label, ovalue, ivalue)

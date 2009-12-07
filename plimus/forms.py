# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

from django import forms

from plimus import models

class PlimusBaseIPNForm(forms.Form):
    def save(self):
        """Return a list of created IPN attributes instead of single model
        """

        refnum = self.data['referenceNumber']

        attrs = []
        for k, v in self.data.items():
            model = self.model(key=k, value=v, reference_number=refnum)
            model.save()

            attrs.append(model)

        return attrs


class PlimusVendorIPNForm(PlimusBaseIPNForm):
    model = models.PlimusVendorIPNAttr

# EOF


# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

from django import forms

from plimus import models

from datetime import datetime

class PlimusBaseIPNForm(forms.Form):
    def save(self):
        """Return a list of created IPN attributes instead of single model
        """

        now = datetime.now()

        refnum = self.data['referenceNumber']

        attrs = []
        for k, v in self.data.items():
            model = self.model(key=k, value=v, reference_number=refnum, tstamp=now)
            model.save()

            attrs.append(model)

        return attrs


class PlimusVendorIPNForm(PlimusBaseIPNForm):
    model = models.PlimusVendorIPNAttr

# EOF


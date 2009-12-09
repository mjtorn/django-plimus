# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

from django.http import HttpResponse

import forms as plimus_forms
import models as plimus_models
import signals as plimus_signals

def plimus_ipn(request):
    data = request.POST.copy() or None

    ipn_form = plimus_forms.PlimusVendorIPNForm(data)

    attrs = ipn_form.save()

    getattr(plimus_signals, data['transactionType'].lower()).send(sender=ipn_form, refnum=data['referenceNumber'], data=plimus_models.PlimusVendorIPNAttr.objects.ipn_dicts(data['referenceNumber'])[-1])

    return HttpResponse('OK!', content_type='text/plain')

# EOF



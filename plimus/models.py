# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

from django.db import models

from datetime import datetime

from decimal import Decimal

class GenericNotificationManager(models.Manager):
    """Allows us to export an Instant Payment/Login Notifications as dicts
    """

    ## Have unicode/string the default, do not set here
    # The spec says "Number #,###.##" for Decimal stuff
    typedict = {
        'testMode': bool,

        'referenceNumber': int,
        'originalReferenceNumber': int,

        'transactionDate': lambda x: datetime.strptime(x, '%m/%d/%Y %H:%M %p'),
        'untilDate': lambda x: datetime.strptime(x, '%m/%d/%Y %H:%M %p') if x else None,

        'productId': int,
        'contractId': int,
        'oldProductId': int,
        'oldContractId': int,
        'newProductId': int,
        'newContractId': int,

        'contractPrice': lambda x: Decimal(x.replace(',', '')),
        'quantity': int,
        'addCD': bool,
        'coupon': bool,
        'couponValue': lambda x: Decimal(x.replace(',', '')),

        'invoiceAmount': lambda x: Decimal(x.replace(',', '')),

        'promoteContractsNum': int,

        'promoteContractId': int,
        'promoteContractPrice': lambda x: Decimal(x.replace(',', '')),

        'promoteContractQuantity': int,

        'accountId': int,
        'userId': int,
    }

    def ipn_dicts(self, refnum):
        """Return data of IPN identified by refnum as dictionary
        """

        from itertools import groupby

        qs = self.filter(reference_number=refnum).order_by('tstamp')

        if not qs:
            raise ValueError('Nothing found for reference number %s' % refnum)

        g = groupby(qs, lambda x: x.tstamp)
        ipn_dict = {}
        ipn_dicts = []
        while True:
            try:
                tstamp, refnum_group = g.next()
                refnum_group = list(refnum_group)

                for ipn_row in refnum_group:
                    key, value = ipn_row.key, ipn_row.value

                    try:
                        value = self.typedict[key](value)
                    except KeyError:
                        if key.startswith('contractId'):
                            value = self.typedict['contractId'](value)
                        elif key.startswith('contractPrice'):
                            value = self.typedict['contractPrice'](value)
                        elif key.startswith('contractQuantity'):
                            value = self.typedict['contractQuantity'](value)

                    ipn_dict[key] = value

                ipn_dicts.append(ipn_dict)

            except StopIteration:
                break

        return ipn_dicts


class PlimusVendorIPNAttr(models.Model):
    """Denormalized Key/Value Pair table
    """

    ## Use this for grouping as refnum is not unique
    ## over transaction types
    tstamp = models.DateTimeField()

    reference_number = models.IntegerField(db_index=True)

    ## The spec has some dynamic keys, so can't limit length
    key = models.TextField()
    ## No String values lengths' are limited in the spec
    value = models.TextField()

    ## Manager too
    objects = GenericNotificationManager()


class PlimusAffiliateIPN(models.Model):
    """Denormalized Key/Value Pair table
    """

    ## Use this for grouping as refnum is not unique
    ## over transaction types
    tstamp = models.DateTimeField()

    reference_number = models.IntegerField(db_index=True)

    ## The spec has some dynamic keys, so can't limit length
    key = models.TextField()
    ## No String values lengths' are limited in the spec
    value = models.TextField()

    ## Manager too
    objects = GenericNotificationManager()


class PlimusLoginCredentialsNotification(models.Model):
    """Denormalized Key/Value Pair table
    """

    account_id = models.IntegerField(db_index=True)

    ## The spec has some dynamic keys, so can't limit length
    key = models.TextField()
    ## No String values lengths' are limited in the spec
    value = models.TextField()

    ## Manager too
    objects = GenericNotificationManager()


# EOF


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
        'untilDate': lambda x: datetime.strptime(x, '%m/%d/%Y %H:%M %p'),

        'productID': int,
        'contractID': int,
        'oldProductID': int,
        'oldContractID': int,
        'newProductID': int,
        'newContractID': int,

        'contractPrice': lambda x: Decimal(x.replace(',', '')),
        'quantity': int,
        'addCD': bool,
        'coupon': bool,
        'couponValue': lambda x: Decimal(x.replace(',', '')),

        'invoiceAmount': lambda x: Decimal(x.replace(',', '')),

        'promoteContractsNum': int,

        'promoteContractID': int,
        'promoteContractPrice': lambda x: Decimal(x.replace(',', '')),

        'promoteContractQuantity': int,

        'accountID': int,
        'userID': int,
    }

    def ipn_as_dict(self, refnum):
        """Return data of IPN identified by refnum as dictionary
        """

        qs = self.filter(reference_number=refnum)

        ipn_dict = {}
        for ipn_row in qs:
            key, value = ipn_row.key, ipn_row.value

            try:
                value = self.typedict[key](value)
            except KeyError:
                if key.startswith('contractID'):
                    value = self.typedict['contractID'](value)
                elif key.startswith('contractPrice'):
                    value = self.typedict['contractPrice'](value)
                elif key.startswith('contractQuantity'):
                    value = self.typedict['contractQuantity'](value)

            ipn_dict[key] = value

        return ipn_dict


class PlimusVendorIPNAttr(models.Model):
    """Denormalized Key/Value Pair table
    """

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


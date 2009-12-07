# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

from django.dispatch import Signal

auth_only = Signal(providing_args=('refnum', 'data'))
charge = Signal(providing_args=('refnum', 'data'))
refund = Signal(providing_args=('refnum', 'data'))
chargeback = Signal(providing_args=('refnum', 'data'))
cancellation = Signal(providing_args=('refnum', 'data'))
recurring = Signal(providing_args=('refnum', 'data'))
cancellation_refund = Signal(providing_args=('refnum', 'data'))
cancellation_chargeback = Signal(providing_args=('refnum', 'data'))
contract_change = Signal(providing_args=('refnum', 'data'))
cancel = Signal(providing_args=('refnum', 'data'))
decline = Signal(providing_args=('refnum', 'data'))

# EOF


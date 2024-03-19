__all__ = ('LoanPoint', 'LoanObjectPoint', 'PaymentPoint', 'EarlyPaymentPoint')

from typing import Union, OrderedDict

from expressmoney.api import *

SERVICE = 'il'


class LoanCreateContract(Contract):
    sign = serializers.IntegerField()
    ip = serializers.IPAddressField()


class LoanReadContract(Contract):
    ISSUING = 'ISSUING'
    OPEN = 'OPEN'  # Customer received money
    OVERDUE = 'OVERDUE'
    STOP_INTERESTS = 'STOP_INTERESTS'
    DEFAULT = "DEFAULT"
    CLOSED = 'CLOSED'
    CANCELED = 'CANCELED'
    STATUS_CHOICES = {
        (ISSUING, ISSUING),
        (OPEN, OPEN),
        (OVERDUE, OVERDUE),
        (STOP_INTERESTS, STOP_INTERESTS),
        (DEFAULT, DEFAULT),
        (CLOSED, CLOSED),
        (CANCELED, CANCELED),
    }
    OPEN_STATUSES = (ISSUING, OPEN, OVERDUE, STOP_INTERESTS, DEFAULT)

    id = serializers.IntegerField(min_value=1)
    created = serializers.DateTimeField()
    updated = serializers.DateTimeField()
    order = serializers.IntegerField(min_value=1)
    status = serializers.ChoiceField(choices=STATUS_CHOICES)
    sign = serializers.IntegerField()
    ip = serializers.IPAddressField()
    interests_limit = serializers.DecimalField(max_digits=3, decimal_places=2)
    document = serializers.CharField(max_length=256, allow_blank=True)

    body_issue = serializers.DecimalField(max_digits=7, decimal_places=0)
    body_paid = serializers.DecimalField(max_digits=7, decimal_places=0)
    body_balance = serializers.DecimalField(max_digits=7, decimal_places=0)
    body_debt = serializers.DecimalField(max_digits=7, decimal_places=0)
    interests_charges = serializers.DecimalField(max_digits=7, decimal_places=0)
    interests_paid = serializers.DecimalField(max_digits=7, decimal_places=0)
    interests_balance = serializers.DecimalField(max_digits=7, decimal_places=0)
    avg_payment = serializers.DecimalField(max_digits=7, decimal_places=0)
    total_interests_overdue = serializers.DecimalField(max_digits=7, decimal_places=0)


class PaymentCreateContract(Contract):
    loan = serializers.IntegerField(min_value=1)
    bank_card_id = serializers.IntegerField(min_value=1)


class EarlyPaymentCreateContract(Contract):
    loan = serializers.IntegerField(min_value=1)
    bank_card_id = serializers.IntegerField(min_value=1)


class LoanID(ID):
    _service = SERVICE
    _app = 'loans'
    _view_set = 'loan'


class PaymentID(ID):
    _service = SERVICE
    _app = 'loans'
    _view_set = 'payment'


class EarlyPaymentID(ID):
    _service = SERVICE
    _app = 'loans'
    _view_set = 'early_payment'


class LoanPoint(ListPointMixin, CreatePointMixin, ContractPoint):
    _point_id = LoanID()
    _read_contract = LoanReadContract
    _create_contract = LoanCreateContract

    def open_loans(self) -> tuple:
        return self.filter(status=self._read_contract.OPEN_STATUSES)

    def open_loans_last(self) -> Union[None, OrderedDict]:
        objects = self.open_loans()
        return objects[-1] if len(objects) > 0 else None


class LoanObjectPoint(RetrievePointMixin, ContractObjectPoint):
    _point_id = LoanID()
    _read_contract = LoanReadContract


class PaymentPoint(CreatePointMixin, ContractPoint):
    _point_id = PaymentID()
    _create_contract = PaymentCreateContract


class EarlyPaymentPoint(CreatePointMixin, ContractPoint):
    _point_id = EarlyPaymentID()
    _create_contract = EarlyPaymentCreateContract

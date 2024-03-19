__all__ = ('LoanPoint', 'LoanObjectPoint', 'ClosedLoanPoint', 'ClosedLoanObjectPoint', 'LoanPaymentPoint',
           'ExportPoint', 'PartialLoanPaymentPoint', 'ExtendLoanPoint', 'RestructureLoanPoint', 'ValidateLoanPoint',
           'PublicPaymentPoint', 'CallBackPaymentPoint', 'LoanContractDataPoint',
           )

from typing import OrderedDict, Union

from expressmoney.api import *

SERVICE = 'loans'


class CommonLoan(Contract):
    ISSUING = 'ISSUING'
    OPEN = "OPEN"  # Customer received money
    OVERDUE = "OVERDUE"
    STOP_INTEREST = "STOP_INTEREST"
    DEFAULT = "DEFAULT"
    CLOSED = "CLOSED"
    CANCELED = 'CANCELED'
    STATUS_CHOICES = {
        (ISSUING, ISSUING),
        (OPEN, "Open"),
        (OVERDUE, "Overdue"),
        (STOP_INTEREST, "Stop interest"),
        (DEFAULT, "Default"),
        (CLOSED, "Closed"),
        (CANCELED, CANCELED),
    }
    OPEN_STATUSES = (ISSUING, OPEN, OVERDUE, STOP_INTEREST, DEFAULT)

    id = serializers.IntegerField(min_value=1)
    created = serializers.DateTimeField()
    updated = serializers.DateTimeField()
    order = serializers.IntegerField(min_value=1)
    interests_charged_date = serializers.DateField(allow_null=True)
    status = serializers.ChoiceField(choices=STATUS_CHOICES)
    sign = serializers.IntegerField()
    ip = serializers.IPAddressField()
    document = serializers.CharField(max_length=256, allow_blank=True)
    comment = serializers.CharField(max_length=2048, allow_blank=True)

    amount = serializers.DecimalField(max_digits=16, decimal_places=0)
    period = serializers.IntegerField(min_value=0)
    free_period = serializers.IntegerField(min_value=0)
    interests = serializers.DecimalField(max_digits=3, decimal_places=2)
    expiry_date = serializers.DateField()
    expiry_period = serializers.IntegerField(min_value=0)
    body_balance = serializers.DecimalField(max_digits=16, decimal_places=0)
    body_paid = serializers.DecimalField(max_digits=16, decimal_places=0)
    interests_total = serializers.DecimalField(max_digits=16, decimal_places=0)
    interests_paid = serializers.DecimalField(max_digits=16, decimal_places=0)
    interests_balance = serializers.DecimalField(max_digits=16, decimal_places=0)


class LoanReadContract(CommonLoan):
    pass


class LoanCreateContract(Contract):
    sign = serializers.IntegerField()
    ip = serializers.IPAddressField()


class ClosedLoanReadContract(CommonLoan):
    pass


class LoanPaymentReadContract(Contract):
    LOAN_BODY = 'LOAN_BODY'
    LOAN_INTERESTS = 'LOAN_INTERESTS'
    LOAN_ISSUE = 'LOAN_ISSUE'

    TYPE_CHOICES = {
        (LOAN_BODY, LOAN_BODY),
        (LOAN_INTERESTS, LOAN_BODY),
        (LOAN_ISSUE, LOAN_BODY),
    }

    id = serializers.IntegerField(min_value=1)
    created = serializers.DateTimeField()
    updated = serializers.DateTimeField()
    loan = serializers.IntegerField(min_value=1)
    type = serializers.ChoiceField(choices=TYPE_CHOICES)
    amount = serializers.DecimalField(max_digits=16, decimal_places=0, min_value=1)
    bank_card_id = serializers.IntegerField(min_value=1)
    bank_card_payment_id = serializers.IntegerField(min_value=1)


class LoanPaymentCreateContract(Contract):
    loan = serializers.IntegerField(min_value=1)
    bank_card_id = serializers.IntegerField(min_value=1)


class OrderFieldContract(Contract):
    NEW = 'NEW'
    DECLINED = 'DECLINED'
    LOAN_CREATED = 'LOAN_CREATED'
    CANCELED = "CANCELED"
    EXPIRED = 'EXPIRED'
    STATUS_CHOICES = (
        (NEW, NEW),
        (DECLINED, DECLINED),
        (LOAN_CREATED, LOAN_CREATED),
        (CANCELED, CANCELED),
        (EXPIRED, EXPIRED),
    )

    id = serializers.IntegerField(min_value=1)
    created = serializers.DateTimeField()
    user_id = serializers.IntegerField(min_value=1)
    amount_approved = serializers.DecimalField(max_digits=7,
                                               decimal_places=0,
                                               allow_null=True,
                                               )
    period_approved = serializers.IntegerField(allow_null=True)
    status = serializers.ChoiceField(choices=STATUS_CHOICES)


class ExportReadContract(Contract):
    ISSUING = 'ISSUING'
    OPEN = "OPEN"  # Customer received money
    OVERDUE = "OVERDUE"
    STOP_INTEREST = "STOP_INTEREST"
    DEFAULT = "DEFAULT"
    CLOSED = "CLOSED"
    CANCELED = 'CANCELED'
    STATUS_CHOICES = {
        (ISSUING, ISSUING),
        (OPEN, "Open"),
        (OVERDUE, "Overdue"),
        (STOP_INTEREST, "Stop interest"),
        (DEFAULT, "Default"),
        (CLOSED, "Closed"),
        (CANCELED, CANCELED),
    }

    id = serializers.IntegerField(min_value=1)
    created = serializers.DateTimeField()
    order = OrderFieldContract()
    status = serializers.ChoiceField(choices=STATUS_CHOICES)


class ExtendLoanCreateContract(Contract):
    pass


class PartialPaymentContract(Contract):
    bank_card_id = serializers.IntegerField(min_value=1)
    amount = serializers.DecimalField(max_digits=16, decimal_places=0)


class RestructureLoanCreateContract(Contract):
    pass


class RestructureLoanReadContract(Contract):
    ACTIVE = 'ACTIVE'
    EXPIRED = 'EXPIRED'
    COMPLETED = 'COMPLETED'
    CANCELED = 'CANCELED'
    STATUS_CHOICES = {
        (ACTIVE, ACTIVE),
        (EXPIRED, EXPIRED),
        (COMPLETED, COMPLETED),
        (CANCELED, CANCELED),
    }
    id = serializers.IntegerField(min_value=1)
    created = serializers.DateTimeField()
    loan = serializers.IntegerField(min_value=1)
    status = serializers.ChoiceField(choices=STATUS_CHOICES)
    start_interests_balance = serializers.DecimalField(max_digits=7, decimal_places=0)
    restructure_schedules = serializers.ListField()


class ValidateLoanCreateContract(Contract):
    loan_id = serializers.IntegerField(min_value=1)


class ValidateLoanResponseContract(Contract):
    loan_id = serializers.IntegerField(min_value=1)
    user_id = serializers.IntegerField(min_value=0)


class PublicPaymentCreateContract(Contract):
    loan_id = serializers.IntegerField(min_value=1)
    amount = serializers.DecimalField(max_digits=16, decimal_places=0)
    payers_service_fee = serializers.DecimalField(max_digits=16, decimal_places=2, min_value=0)
    payment_id = serializers.IntegerField()


class CallBackPaymentCreateContract(Contract):
    amount = serializers.DecimalField(max_digits=16, decimal_places=0)
    payment_id = serializers.IntegerField()


class LoanContractDataCreateContract(Contract):
    loan_id = serializers.IntegerField(min_value=1)


class CallBackPaymentResponseContract(Contract):
    id = serializers.IntegerField()
    type = serializers.CharField(max_length=32)


class PublicPaymentResponseContract(Contract):
    id = serializers.IntegerField()
    type = serializers.CharField(max_length=32)


class LoanContractDataResponseContract(Contract):
    data_for_pdf = serializers.JSONField()


class RestructureLoanID(ID):
    _service = SERVICE
    _app = 'loans'
    _view_set = 'restructure_loan'


class LoanID(ID):
    _service = SERVICE
    _app = 'loans'
    _view_set = 'loan'


class ClosedLoanID(ID):
    _service = SERVICE
    _app = 'loans'
    _view_set = 'closed_loan'


class LoanPaymentID(ID):
    _service = SERVICE
    _app = 'loans'
    _view_set = 'loan_payment'


class ExportID(ID):
    _service = SERVICE
    _app = 'loans'
    _view_set = 'export'


class ExtendLoanID(ID):
    _service = SERVICE
    _app = 'loans'
    _view_set = 'set_extended'


class PartialPaymentID(ID):
    _service = SERVICE
    _app = 'loans'
    _view_set = 'partial_payment'


class ValidateLoanID(ID):
    _service = SERVICE
    _app = 'loans'
    _view_set = 'validate_loan'


class PublicPaymentID(ID):
    _service = SERVICE
    _app = 'loans'
    _view_set = 'public_payment'


class CallBackPaymentID(ID):
    _service = SERVICE
    _app = 'loans'
    _view_set = 'call_back_payment'


class LoanContractDataID(ID):
    _service = SERVICE
    _app = 'loans'
    _view_set = 'loan_contract_data'


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


class ClosedLoanPoint(ListPointMixin, ContractPoint):
    _point_id = ClosedLoanID()
    _read_contract = ClosedLoanReadContract


class ClosedLoanObjectPoint(RetrievePointMixin, ContractObjectPoint):
    _point_id = ClosedLoanID()
    _read_contract = ClosedLoanReadContract


class LoanPaymentPoint(ListPointMixin, CreatePointMixin, ContractPoint):
    _point_id = LoanPaymentID()
    _read_contract = LoanPaymentReadContract
    _create_contract = LoanPaymentCreateContract


class ExportPoint(ListPointMixin, ContractPoint):
    _point_id = ExportID()
    _read_contract = ExportReadContract
    _cache_enabled = False


class ExtendLoanPoint(CreatePointMixin, ContractPoint):
    _point_id = ExtendLoanID()
    _create_contract = ExtendLoanCreateContract


class PartialLoanPaymentPoint(CreatePointMixin, ContractPoint):
    _point_id = PartialPaymentID()
    _create_contract = PartialPaymentContract


class RestructureLoanPoint(CreatePointMixin, ListPointMixin, ContractPoint):
    _point_id = RestructureLoanID()
    _create_contract = RestructureLoanCreateContract
    _read_contract = RestructureLoanReadContract


class ValidateLoanPoint(CreatePointMixin, ResponseMixin, ContractPoint):
    _point_id = ValidateLoanID()
    _create_contract = ValidateLoanCreateContract
    _response_contract = ValidateLoanResponseContract


class PublicPaymentPoint(CreatePointMixin, ResponseMixin, ContractPoint):
    _point_id = PublicPaymentID()
    _create_contract = PublicPaymentCreateContract
    _response_contract = PublicPaymentResponseContract


class CallBackPaymentPoint(CreatePointMixin, ResponseMixin, ContractPoint):
    _point_id = CallBackPaymentID()
    _create_contract = CallBackPaymentCreateContract
    _response_contract = CallBackPaymentResponseContract


class LoanContractDataPoint(CreatePointMixin, ResponseMixin, ContractPoint):
    _point_id = LoanContractDataID()
    _create_contract = LoanContractDataCreateContract
    _response_contract = LoanContractDataResponseContract

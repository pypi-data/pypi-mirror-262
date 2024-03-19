__all__ = ('BankCardPaymentPoint', 'PublicBankCardPaymentPoint', 'PaymentInvoicePoint', 'PublicTransaction3DSPoint',
           'BankCardPaymentWithFeePoint', 'CreditRatingReceiptPoint')

from expressmoney.api import *

SERVICE = 'payments'


class BankCardPaymentCreateContract(Contract):
    amount = serializers.DecimalField(max_digits=16, decimal_places=0, min_value=1)
    withdraw = serializers.BooleanField()
    bank_card = serializers.IntegerField(min_value=1)
    order_id = serializers.IntegerField()
    order_type = serializers.CharField(max_length=128)


class BankCardPaymentWithFeeCreateContract(Contract):
    amount = serializers.DecimalField(max_digits=16, decimal_places=0, min_value=1)
    payers_service_fee = serializers.DecimalField(max_digits=16, decimal_places=2, min_value=1)
    withdraw = serializers.BooleanField()
    bank_card = serializers.IntegerField(min_value=1)
    order_id = serializers.IntegerField()
    order_type = serializers.CharField(max_length=128)
    loan_id = serializers.IntegerField(allow_null=True)
    loan_created = serializers.DateTimeField(allow_null=True)


class PaymentInvoiceCreateContract(Contract):
    amount = serializers.DecimalField(max_digits=7, decimal_places=0)
    loan_type = serializers.CharField(max_length=16)
    description = serializers.CharField(max_length=512)


class PublicTransaction3DSCreateContract(Contract):
    amount = serializers.DecimalField(max_digits=16, decimal_places=0, min_value=1)
    ip = serializers.IPAddressField()
    cryptogram = serializers.CharField(max_length=2048)
    loan_id = serializers.IntegerField(min_value=1)
    user_id = serializers.IntegerField(min_value=1)


class PaymentInvoiceResponseContract(Contract):
    id = serializers.IntegerField(min_value=1)
    url = serializers.CharField(max_length=512)


class BankCardPaymentResponseContract(Contract):
    id = serializers.IntegerField(min_value=1)
    created = serializers.DateTimeField()


class BankCardPaymentWithFeeResponseContract(Contract):
    id = serializers.IntegerField(min_value=1)
    created = serializers.DateTimeField()


class BankCardPaymentReadContract(BankCardPaymentCreateContract):
    id = serializers.IntegerField(min_value=1)
    created = serializers.DateTimeField()


class PublicBankCardPaymentCreateContract(Contract):
    md = serializers.CharField(max_length=8192)
    pa_res = serializers.CharField(max_length=8192)


class PublicTransaction3DSResponseContract(Contract):
    acs_url = serializers.URLField(required=False)
    pa_req = serializers.CharField(required=False)
    transaction_id = serializers.CharField(required=False)


class CreditRatingReceiptCreateContract(Contract):
    amount = serializers.DecimalField(max_digits=16, decimal_places=2, min_value=1)


class CreditRatingReceiptResponseContract(Contract):
    receipt_id = serializers.CharField(max_length=32)


class BankCardPaymentID(ID):
    _service = SERVICE
    _app = 'payments'
    _view_set = 'bank_card_payment'


class PaymentInvoiceID(ID):
    _service = SERVICE
    _app = 'payments'
    _view_set = 'payment_invoice'


class PublicBankCardPaymentID(ID):
    _service = SERVICE
    _app = 'payments'
    _view_set = 'bank_card_public_payment'


class PublicTransaction3DSID(ID):
    _service = SERVICE
    _app = 'payments'
    _view_set = 'public_transaction_3ds'


class BankCardPaymentWithFeeID(ID):
    _service = SERVICE
    _app = 'payments'
    _view_set = 'bank_card_payment_with_fee'


class CreditRatingReceiptID(ID):
    _service = SERVICE
    _app = 'payments'
    _view_set = 'credit_rating_receipt'


class BankCardPaymentPoint(ListPointMixin, ResponseMixin, CreatePointMixin, ContractPoint):
    _point_id = BankCardPaymentID()
    _create_contract = BankCardPaymentCreateContract
    _response_contract = BankCardPaymentResponseContract
    _read_contract = BankCardPaymentReadContract


class PaymentInvoicePoint(CreatePointMixin, ResponseMixin, ContractPoint):
    _point_id = PaymentInvoiceID()
    _create_contract = PaymentInvoiceCreateContract
    _response_contract = PaymentInvoiceResponseContract


class PublicBankCardPaymentPoint(CreatePointMixin, ContractPoint):
    _point_id = PublicBankCardPaymentID()
    _create_contract = PublicBankCardPaymentCreateContract


class PublicTransaction3DSPoint(ResponseMixin, CreatePointMixin, ContractPoint):
    _point_id = PublicTransaction3DSID()
    _create_contract = PublicTransaction3DSCreateContract
    _response_contract = PublicTransaction3DSResponseContract


class BankCardPaymentWithFeePoint(ResponseMixin, CreatePointMixin, ContractPoint):
    _point_id = BankCardPaymentWithFeeID()
    _create_contract = BankCardPaymentWithFeeCreateContract
    _response_contract = BankCardPaymentWithFeeResponseContract


class CreditRatingReceiptPoint(CreatePointMixin, ResponseMixin, ContractPoint):
    _point_id = CreditRatingReceiptID()
    _create_contract = CreditRatingReceiptCreateContract
    _response_contract = CreditRatingReceiptResponseContract

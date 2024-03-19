__all__ = ('BankCardPoint', 'BankCard3dsPoint', 'ActivatePoint', 'LogPoint')

from expressmoney.api import *

SERVICE = 'payments'


class GenericBankCard(Contract):
    bin = serializers.CharField(max_length=6)
    number = serializers.CharField(max_length=4)
    expiry_month = serializers.IntegerField(min_value=1, max_value=12)
    expiry_year = serializers.IntegerField(min_value=20, max_value=100)


class BankCardCreateContract(GenericBankCard):
    ip = serializers.IPAddressField()
    cryptogram = serializers.CharField(max_length=2048)


class ActivateCreateContract(Contract):
    bank_card = serializers.IntegerField(min_value=1)


class BankCardResponseContract(Contract):
    acs_url = serializers.URLField(required=False)
    pa_req = serializers.CharField(required=False)
    md = serializers.CharField(required=False)


class BankCardReadContract(GenericBankCard):
    PAYPAL = "PAYPAL"
    CLOUDPAYMENTS = "CLOUDPAYMENTS"
    GATEWAY_CHOICES = (
        (PAYPAL, "PayPal"),
        (CLOUDPAYMENTS, "CloudPayments")
    )
    id = serializers.IntegerField(min_value=1)
    created = serializers.DateTimeField()
    is_active = serializers.BooleanField()


class BankCard3dsContract(Contract):
    md = serializers.CharField(max_length=8192)
    pa_res = serializers.CharField(max_length=8192)


class LogCreateContract(Contract):
    bank_card = serializers.CharField(max_length=128)


class BankCardID(ID):
    _service = SERVICE
    _app = 'bank_cards'
    _view_set = 'bank_card'


class BankCard3dsID(ID):
    _service = SERVICE
    _app = 'bank_cards'
    _view_set = 'bank_card_3ds'


class ActivateID(ID):
    _service = SERVICE
    _app = 'bank_cards'
    _view_set = 'activate'


class LogID(ID):
    _service = SERVICE
    _app = 'bank_cards'
    _view_set = 'log'


class BankCardPoint(ListPointMixin, ResponseMixin, CreatePointMixin, ContractPoint):
    _point_id = BankCardID()
    _create_contract = BankCardCreateContract
    _response_contract = BankCardResponseContract
    _read_contract = BankCardReadContract


class BankCard3dsPoint(CreatePointMixin, ContractPoint):
    _point_id = BankCard3dsID()
    _create_contract = BankCard3dsContract


class ActivatePoint(CreatePointMixin, ContractPoint):
    _point_id = ActivateID()
    _create_contract = ActivateCreateContract


class LogPoint(CreatePointMixin, ContractPoint):
    _point_id = LogID()
    _create_contract = LogCreateContract

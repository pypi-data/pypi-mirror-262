__all__ = ('LoanPostBackPoint', 'OrderPostBackPoint', 'LoanClientPostBackPoint', 'OrderClientPostBackPoint',
           'CPAClientObjectPoint', 'CPACUserObjectPoint')

from expressmoney.api import *

SERVICE = 'cpa'

from phonenumber_field.serializerfields import PhoneNumberField


class CPAClientReadContract(Contract):
    utm_source = serializers.CharField(max_length=128)
    transaction_id = serializers.CharField(max_length=256, allow_blank=True)


class CPAUserReadContract(Contract):
    first_name = serializers.CharField(max_length=32, allow_blank=True)
    last_name = serializers.CharField(max_length=32, allow_blank=True)
    middle_name = serializers.CharField(max_length=32, allow_blank=True)
    birth_date = serializers.DateField()
    phone_number = PhoneNumberField()
    utm_source = serializers.CharField(max_length=128)
    click_id = serializers.CharField(max_length=256, allow_blank=True)


class LoanPostBackCreateContract(Contract):
    loan_id = serializers.IntegerField()
    phone_number = PhoneNumberField()
    amount = serializers.DecimalField(max_digits=16, decimal_places=0)


class OrderPostBackCreateContract(Contract):
    order_id = serializers.IntegerField()
    phone_number = PhoneNumberField()
    amount = serializers.DecimalField(max_digits=16, decimal_places=0)


class LoanClientPostBackCreateContract(Contract):
    loan_id = serializers.IntegerField()
    utm_source = serializers.CharField(max_length=128, allow_blank=True)
    transaction_id = serializers.CharField(max_length=256, allow_blank=True)
    amount = serializers.DecimalField(max_digits=16, decimal_places=0)


class OrderClientPostBackCreateContract(Contract):
    order_id = serializers.IntegerField()
    utm_source = serializers.CharField(max_length=128, allow_blank=True)
    transaction_id = serializers.CharField(max_length=256, allow_blank=True)
    amount = serializers.DecimalField(max_digits=16, decimal_places=0)


class LoanPostBackResponseContract(Contract):
    pass


class LoanClientPostBackResponseContract(Contract):
    pass


class LoanPostBackID(ID):
    _service = SERVICE
    _app = 'cpas'
    _view_set = 'loan_post_back'


class OrderPostBackID(ID):
    _service = SERVICE
    _app = 'cpas'
    _view_set = 'order_post_back'


class LoanClientPostBackID(ID):
    _service = SERVICE
    _app = 'cpas'
    _view_set = 'loan_client_post_back'


class OrderClientPostBackID(ID):
    _service = SERVICE
    _app = 'cpas'
    _view_set = 'order_client_post_back'


class CPAClientID(ID):
    _service = SERVICE
    _app = 'cpas'
    _view_set = 'cpa_client'


class CPAUserID(ID):
    _service = SERVICE
    _app = 'cpas'
    _view_set = 'cpa_user'


class LoanPostBackPoint(CreatePointMixin, ResponseMixin, ContractPoint):
    _point_id = LoanPostBackID()
    _create_contract = LoanPostBackCreateContract
    _response_contract = LoanPostBackResponseContract


class OrderPostBackPoint(CreatePointMixin, ContractPoint):
    _point_id = OrderPostBackID()
    _create_contract = OrderPostBackCreateContract


class LoanClientPostBackPoint(CreatePointMixin, ResponseMixin, ContractPoint):
    _point_id = LoanClientPostBackID()
    _create_contract = LoanClientPostBackCreateContract
    _response_contract = LoanClientPostBackResponseContract


class OrderClientPostBackPoint(CreatePointMixin, ContractPoint):
    _point_id = OrderClientPostBackID()
    _create_contract = OrderClientPostBackCreateContract


class CPAClientObjectPoint(RetrievePointMixin, ContractObjectPoint):
    _point_id = CPAClientID()
    _read_contract = CPAClientReadContract


class CPACUserObjectPoint(RetrievePointMixin, ContractObjectPoint):
    _point_id = CPAUserID()
    _read_contract = CPAUserReadContract

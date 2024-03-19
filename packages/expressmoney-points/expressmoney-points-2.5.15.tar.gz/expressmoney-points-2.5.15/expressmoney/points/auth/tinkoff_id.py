__all__ = ('TinkoffIDPoint', 'TokenPoint')

from expressmoney.api import *

from phonenumber_field.serializerfields import PhoneNumberField

SERVICE = 'auth'


class TinkoffIDCreateContract(Contract):
    code = serializers.CharField(max_length=32)


class TinkoffIDResponseContract(Contract):
    access_token = serializers.CharField(max_length=128, allow_blank=True, allow_null=True)
    refresh_token = serializers.CharField(max_length=512, allow_blank=True, allow_null=True)
    confirm_phone = serializers.BooleanField(default=False)
    first_name = serializers.CharField(max_length=32)
    last_name = serializers.CharField(max_length=32)
    middle_name = serializers.CharField(max_length=32)
    phone_number = PhoneNumberField()


class TinkoffID_ID(ID):
    _service = SERVICE
    _app = 'tinkoff_id'
    _view_set = 'tinkoff_id'


class TinkoffIDPoint(CreatePointMixin, ResponseMixin, ContractPoint):
    _point_id = TinkoffID_ID()
    _create_contract = TinkoffIDCreateContract
    _response_contract = TinkoffIDResponseContract


class TokenID(ID):
    _service = SERVICE
    _app = 'tinkoff_id'
    _view_set = 'token'


class TokenCreateContract(Contract):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128)


class TokenResponseContract(Contract):
    refresh = serializers.CharField(max_length=None)
    access = serializers.CharField(max_length=None)


class TokenPoint(CreatePointMixin, ResponseMixin, ContractPoint):
    _point_id = TokenID()
    _create_contract = TokenCreateContract
    _response_contract = TokenResponseContract

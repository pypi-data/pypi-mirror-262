__all__ = ('SmsPoint',)

from expressmoney.api import *
from phonenumber_field.serializerfields import PhoneNumberField

SERVICE = 'notifications'


class SmsCreateContract(Contract):
    message = serializers.CharField(min_length=1, max_length=130)
    phonenumber = PhoneNumberField(required=False)


class SmsID(ID):
    _service = SERVICE
    _app = 'sms'
    _view_set = 'sms'


class SmsPoint(CreatePointMixin, ContractPoint):
    _point_id = SmsID()
    _create_contract = SmsCreateContract

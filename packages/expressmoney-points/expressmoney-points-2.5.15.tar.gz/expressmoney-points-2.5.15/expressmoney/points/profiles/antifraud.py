__all__ = ('LinkPoint', 'NewDevicePoint')

from expressmoney.api import *


SERVICE = 'profiles'
APP = 'antifraud'


class LinkCreateContract(Contract):
    pass


class LinkReadContract(Contract):
    created = serializers.DateTimeField()
    full_name = serializers.IntegerField()
    full_name_black_list = serializers.IntegerField()
    full_name_overdue = serializers.IntegerField()
    document = serializers.IntegerField()
    document_black_list = serializers.IntegerField()
    document_overdue = serializers.IntegerField()
    address = serializers.IntegerField()
    address_black_list = serializers.IntegerField()
    address_overdue = serializers.IntegerField()
    ip = serializers.IntegerField()
    ip_black_list = serializers.IntegerField()
    ip_overdue = serializers.IntegerField()
    fingerprint = serializers.IntegerField()
    fingerprint_black_list = serializers.IntegerField()
    fingerprint_overdue = serializers.IntegerField()
    ga = serializers.IntegerField()
    ga_black_list = serializers.IntegerField()
    ga_overdue = serializers.IntegerField()
    bank_card = serializers.IntegerField()
    bank_card_black_list = serializers.IntegerField()
    bank_card_overdue = serializers.IntegerField()
    ip_fingerprint = serializers.IntegerField()
    ip_fingerprint_black_list = serializers.IntegerField()
    ip_fingerprint_overdue = serializers.IntegerField()


class NewDeviceCreateContract(Contract):
    pass


class NewDeviceResponseContract(Contract):
    is_find = serializers.BooleanField()


class LinkResponseContract(LinkReadContract):
    pass


class LinkID(ID):
    _service = SERVICE
    _app = APP
    _view_set = 'link'


class NewDeviceID(ID):
    _service = SERVICE
    _app = APP
    _view_set = 'new_device'


class LinkPoint(ResponseMixin, ListPointMixin, CreatePointMixin, ContractPoint):
    _point_id = LinkID()
    _create_contract = LinkCreateContract
    _read_contract = LinkReadContract
    _response_contract = LinkResponseContract


class NewDevicePoint(ResponseMixin, CreatePointMixin, ContractPoint):
    _point_id = NewDeviceID()
    _create_contract = NewDeviceCreateContract
    _response_contract = NewDeviceResponseContract

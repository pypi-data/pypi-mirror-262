__all__ = ('WhiteListPoint', 'WhiteListObjectPoint')

from expressmoney.api import *
from expressmoney.api.point import DestroyPointMixin

SERVICE = 'loans'
APP = 'antifraud'


class WhiteListCreateContract(Contract):
    comment = serializers.CharField(max_length=128, allow_blank=True)


class WhiteListReadContract(WhiteListCreateContract):
    created = serializers.DateTimeField()


class WhiteListID(ID):
    _service = SERVICE
    _app = APP
    _view_set = 'white_list'


class WhiteListPoint(CreatePointMixin, ContractPoint):
    _point_id = WhiteListID()
    _read_contract = WhiteListReadContract
    _create_contract = WhiteListCreateContract


class WhiteListObjectPoint(DestroyPointMixin, RetrievePointMixin, ContractObjectPoint):
    _point_id = WhiteListID()
    _read_contract = WhiteListReadContract

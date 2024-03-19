__all__ = ('BlackListPoint',)

from expressmoney.api import *

SERVICE = 'loc'
APP = 'black_list'


class BlackListCreateContract(Contract):
    comment = serializers.CharField(max_length=128, allow_blank=True)


class BlackListID(ID):
    _service = SERVICE
    _app = APP
    _view_set = 'black_list'


class BlackListPoint(CreatePointMixin, ContractPoint):
    _point_id = BlackListID()
    _create_contract = BlackListCreateContract

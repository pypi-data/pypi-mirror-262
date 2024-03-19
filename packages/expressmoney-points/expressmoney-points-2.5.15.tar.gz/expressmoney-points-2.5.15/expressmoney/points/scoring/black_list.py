__all__ = ('BlackListPoint', )

from expressmoney.api import *


SERVICE = 'scoring'
APP = 'black_list'


class BlackListReadContract(Contract):
    created = serializers.DateTimeField()
    passport_serial = serializers.CharField(max_length=4)
    passport_number = serializers.CharField(max_length=6)
    scoring = serializers.IntegerField()
    comment = serializers.CharField(max_length=128, allow_blank=True)


class BlackListID(ID):
    _service = SERVICE
    _app = APP
    _view_set = 'black_list'


class BlackListPoint(ListPointMixin, ContractPoint):
    _point_id = BlackListID()
    _read_contract = BlackListReadContract
    _sort_by = 'created'
    _cache_enabled = False

__all__ = ('EfinViewFlowTaskPoint', )

from expressmoney.api import *

SERVICE = 'profiles'
APP = 'signing'


class _EfinViewFlowTaskCreateContract(Contract):
    contract_photo_1 = serializers.CharField(max_length=256)
    contract_photo_2 = serializers.CharField(max_length=256)
    passport_photo_1 = serializers.CharField(max_length=256)
    passport_photo_2 = serializers.CharField(max_length=256)
    client_photo = serializers.CharField(max_length=256)
    efin_order_id = serializers.IntegerField()
    sign_day = serializers.DateField()


class _EfinViewFlowTask(ID):
    _service = SERVICE
    _app = APP
    _view_set = 'efin_view_flow_task'


class EfinViewFlowTaskPoint(CreatePointMixin, ContractPoint):
    _point_id = _EfinViewFlowTask()
    _create_contract = _EfinViewFlowTaskCreateContract

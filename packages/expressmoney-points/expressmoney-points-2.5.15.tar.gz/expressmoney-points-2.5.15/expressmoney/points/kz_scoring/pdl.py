__all__ = ('ScoringPoint', )

from expressmoney.api import *


SERVICE = 'kz-scoring'
APP = 'pdl'


class ScoringCreateContract(Contract):
    order_id = serializers.CharField(max_length=32, allow_null=True)
    period_requested = serializers.IntegerField(min_value=1, max_value=500)
    amount_requested = serializers.IntegerField(min_value=1000, max_value=200000)
    # Loans data
    total_loans = serializers.IntegerField(min_value=0)
    interests_sum = serializers.IntegerField(min_value=0)
    body_sum = serializers.IntegerField(min_value=0)
    body_max = serializers.IntegerField(min_value=0)


class ScoringResponseContract(Contract):
    amount_approved = serializers.IntegerField(allow_null=True)


class ScoringID(ID):
    _service = SERVICE
    _app = APP
    _view_set = 'scoring'


class ScoringPoint(ResponseMixin, CreatePointMixin, ContractPoint):
    _point_id = ScoringID()
    _create_contract = ScoringCreateContract
    _response_contract = ScoringResponseContract

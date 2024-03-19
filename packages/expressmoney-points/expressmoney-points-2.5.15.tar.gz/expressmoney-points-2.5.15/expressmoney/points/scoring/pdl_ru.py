__all__ = ('ScoringPoint', 'ScoringObjectPoint', 'StatusPredictPoint', 'StatusPredictObjectPoint')

from expressmoney.api import *


SERVICE = 'scoring'
APP = 'pdl_ru'


class ScoringCreateContract(Contract):
    order_id = serializers.CharField(max_length=32, allow_null=True)
    period_requested = serializers.IntegerField(min_value=1, max_value=500)
    amount_requested = serializers.IntegerField(min_value=1000, max_value=200000)
    department = serializers.CharField(max_length=128, allow_null=True)

    first_name = serializers.CharField(max_length=32, min_length=1)
    last_name = serializers.CharField(max_length=32, min_length=1)
    middle_name = serializers.CharField(max_length=32)
    birth_date = serializers.DateField()
    passport_serial = serializers.CharField(max_length=4, min_length=4)
    passport_number = serializers.CharField(max_length=6, min_length=6)
    passport_date = serializers.DateField()
    passport_code = serializers.CharField(max_length=7, min_length=7)
    snils = serializers.CharField(max_length=16, allow_blank=True)
    # Loans data
    total_loans = serializers.IntegerField(min_value=0)
    interests_sum = serializers.IntegerField(min_value=0)
    body_sum = serializers.IntegerField(min_value=0)
    body_max = serializers.IntegerField(min_value=0)


class ScoringModelContract(Contract):
    created = serializers.DateTimeField()
    updated = serializers.DateTimeField()
    model_name = serializers.CharField(max_length=32)
    score_min = serializers.DecimalField(max_digits=3, decimal_places=2)
    comment = serializers.CharField(max_length=1024)


class ScoringReadContract(ScoringCreateContract):
    created = serializers.DateTimeField(allow_null=True)
    score = serializers.DecimalField(max_digits=3, decimal_places=2, allow_null=True)
    score_min = serializers.DecimalField(max_digits=3, decimal_places=2, allow_null=True)
    amount_approved = serializers.IntegerField(allow_null=True)
    scoring_model_approved = ScoringModelContract(allow_null=True)


class ScoringResponseContract(ScoringCreateContract):
    score = serializers.DecimalField(max_digits=3, decimal_places=2, allow_null=True)
    score_min = serializers.DecimalField(max_digits=3, decimal_places=2, allow_null=True)
    amount_approved = serializers.IntegerField(allow_null=True)
    scoring_model_approved = ScoringModelContract(allow_null=True)


class ScoringUpdateContract(Contract):
    status = serializers.CharField(max_length=32)
    status_date = serializers.DateField(allow_null=True)


class StatusPredictUpdateContract(Contract):
    status_predict = serializers.CharField(max_length=32)


class ScoringID(ID):
    _service = SERVICE
    _app = APP
    _view_set = 'scoring'


class StatusPredictID(ID):
    _service = SERVICE
    _app = APP
    _view_set = 'status_predict'


class ScoringPoint(ListPointMixin,
                   ResponseMixin,
                   CreatePointMixin,
                   ContractPoint):
    _point_id = ScoringID()
    _create_contract = ScoringCreateContract
    _read_contract = ScoringReadContract
    _response_contract = ScoringResponseContract
    _sort_by = 'created'
    _cache_enabled = False


class ScoringObjectPoint(RetrievePointMixin, UpdatePointMixin,
                         ContractObjectPoint):
    _point_id = ScoringID()
    _read_contract = ScoringReadContract
    _update_contract = ScoringUpdateContract
    _cache_enabled = False


class StatusPredictPoint(ListPointMixin, ContractPoint):
    _point_id = StatusPredictID()
    _read_contract = ScoringReadContract
    _sort_by = 'created'
    _cache_enabled = False


class StatusPredictObjectPoint(UpdatePointMixin, ContractObjectPoint):
    _point_id = StatusPredictID()
    _update_contract = StatusPredictUpdateContract
    _cache_enabled = False

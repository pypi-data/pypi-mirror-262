__all__ = ('RussianSelfEmploymentContractPoint',)

from expressmoney.api import *

SERVICE = 'partners'
APP = 'contracts'


class RussianSelfEmploymentCreateContract(Contract):
    inn = serializers.CharField(max_length=32)


class RussianSelfEmploymentReadContract(RussianSelfEmploymentCreateContract):
    VERIFICATION = 'VERIFICATION'
    CONFIRMED = 'CONFIRMED'
    REJECTED = 'REJECTED'
    STATUS_CHOICES = (
        (VERIFICATION, VERIFICATION),
        (CONFIRMED, CONFIRMED),
        (REJECTED, REJECTED),
    )
    id = serializers.IntegerField(min_value=1)
    created = serializers.DateTimeField()
    updated = serializers.DateTimeField()
    document = serializers.CharField(max_length=256, allow_blank=True)
    status = serializers.ChoiceField(choices=STATUS_CHOICES)


class RussianSelfEmploymentContractID(ID):
    _service = SERVICE
    _app = APP
    _view_set = 'russian_self_employment_contract'


class RussianSelfEmploymentContractPoint(CreatePointMixin, ListPointMixin, ContractPoint):
    _point_id = RussianSelfEmploymentContractID()
    _create_contract = RussianSelfEmploymentCreateContract
    _read_contract = RussianSelfEmploymentReadContract
    _sort_by = 'created'

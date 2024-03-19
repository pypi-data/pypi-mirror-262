__all__ = ('PartnerPoint', 'PartnerObjectPoint',
           'PartnerByReferralObjectPoint')

from django.core.validators import RegexValidator
from expressmoney.api import *

SERVICE = 'partners'
APP = 'partners'


class PartnerCreateContract(Contract):
    pass


class PartnerUpdateContract(Contract):
    code = serializers.CharField(max_length=8,
                                 validators=(
                                     RegexValidator(regex='^[A-Z0-9]*$',
                                                    message='invalid_format',
                                                    code='invalid_format'
                                                    ),),
                                 )


class RewardSerializer(serializers.Serializer):
    action_name = serializers.CharField(max_length=64)
    amount = serializers.DecimalField(decimal_places=0, max_digits=16)
    amount_currency = serializers.CharField(max_length=8)


class PartnerReadContract(PartnerUpdateContract):
    created = serializers.DateTimeField()
    balance = serializers.DecimalField(max_digits=16, decimal_places=1)
    is_trusted = serializers.BooleanField()
    rating = serializers.CharField(max_length=24, allow_null=True)
    reward = RewardSerializer(many=True, allow_null=True, required=False)


class PartnerID(ID):
    _service = SERVICE
    _app = APP
    _view_set = 'partner'


class PartnerByReferralID(ID):
    _service = SERVICE
    _app = APP
    _view_set = 'partner_by_referral'


class PartnerPoint(CreatePointMixin, ContractPoint):
    _point_id = PartnerID()
    _create_contract = PartnerCreateContract


class PartnerObjectPoint(RetrievePointMixin, UpdatePointMixin,
                         ContractObjectPoint):
    _point_id = PartnerID()
    _read_contract = PartnerReadContract
    _update_contract = PartnerUpdateContract


class PartnerByReferralObjectPoint(RetrievePointMixin, ContractObjectPoint):
    _point_id = PartnerByReferralID()
    _read_contract = PartnerReadContract

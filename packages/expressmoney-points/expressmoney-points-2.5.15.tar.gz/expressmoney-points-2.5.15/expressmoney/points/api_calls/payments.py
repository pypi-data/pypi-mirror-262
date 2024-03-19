__all__ = ('PartnerBankCardIdPoint', )

from expressmoney.api import *

SERVICE = 'api-calls'
APP = 'payments'


class PartnerBankCardIdCreateContract(Contract):
    bank_card_id = serializers.IntegerField()


class PartnerBankCardIdID(ID):
    _service = SERVICE
    _app = APP
    _view_set = 'partner_bank_card_id'


class PartnerBankCardIdPoint(CreatePointMixin, ContractPoint):
    _point_id = PartnerBankCardIdID()
    _create_contract = PartnerBankCardIdCreateContract

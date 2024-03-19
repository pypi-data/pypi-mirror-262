__all__ = ('OrderPoint', 'OrderObjectPoint', 'ResendSmsSignPoint', 'OrderUserIdsPoint', 'SetAmountApprovedPoint')

from expressmoney.api import *

SERVICE = 'loans'


class ProductContract(Contract):
    created = serializers.DateTimeField()
    updated = serializers.DateTimeField()
    is_active = serializers.BooleanField()
    free_period = serializers.IntegerField(min_value=0)
    interests = serializers.DecimalField(max_digits=3, decimal_places=2)


class OrderCreateContract(Contract):
    amount_requested = serializers.DecimalField(max_digits=7,
                                                decimal_places=0,
                                                min_value=1000,
                                                max_value=15000,
                                                )
    period_requested = serializers.IntegerField(min_value=3, max_value=30)
    bank_card_id = serializers.IntegerField(min_value=1, allow_null=True)
    promocode_code = serializers.CharField(max_length=16, allow_blank=True)


class OrderReadContract(OrderCreateContract):
    NEW = 'NEW'
    DECLINED = 'DECLINED'
    LOAN_CREATED = 'LOAN_CREATED'
    CANCELED = "CANCELED"
    EXPIRED = 'EXPIRED'
    STATUS_CHOICES = (
        (NEW, NEW),
        (DECLINED, DECLINED),
        (LOAN_CREATED, LOAN_CREATED),
        (CANCELED, CANCELED),
        (EXPIRED, EXPIRED),
    )

    id = serializers.IntegerField(min_value=1)
    created = serializers.DateTimeField()
    updated = serializers.DateTimeField()
    user_id = serializers.IntegerField(min_value=1)
    amount_approved = serializers.DecimalField(max_digits=7,
                                               decimal_places=0,
                                               allow_null=True,
                                               )
    period_approved = serializers.IntegerField(allow_null=True)
    product = ProductContract(allow_null=True)
    status = serializers.ChoiceField(choices=STATUS_CHOICES)
    contract_demo = serializers.CharField(max_length=256, allow_blank=True)


class ResendSmsSignCreateContract(Contract):
    pass


class OrderUserIdsContract(Contract):
    id = serializers.IntegerField(min_value=1)
    user_id = serializers.IntegerField()


class SetAmountApprovedContract(Contract):
    order = serializers.IntegerField()


class OrderID(ID):
    _service = SERVICE
    _app = 'orders'
    _view_set = 'order'


class ResendSmsSignPointID(ID):
    _service = SERVICE
    _app = 'orders'
    _view_set = 'resend_sms_sign'


class OrderUserIdsID(ID):
    _service = SERVICE
    _app = 'orders'
    _view_set = 'order_user_ids'


class SetAmountApprovedID(ID):
    _service = SERVICE
    _app = 'orders'
    _view_set = 'set_amount_approved'


class OrderPoint(ListPointMixin, CreatePointMixin, ContractPoint):
    _point_id = OrderID()
    _read_contract = OrderReadContract
    _create_contract = OrderCreateContract


class OrderObjectPoint(RetrievePointMixin, ContractObjectPoint):
    _point_id = OrderID()
    _read_contract = OrderReadContract


class ResendSmsSignPoint(CreatePointMixin, ContractPoint):
    _point_id = ResendSmsSignPointID()
    _create_contract = ResendSmsSignCreateContract


class OrderUserIdsPoint(ListPointMixin, ContractPoint):
    _point_id = OrderUserIdsID()
    _read_contract = OrderUserIdsContract
    _cache_enabled = False


class SetAmountApprovedPoint(CreatePointMixin, ContractPoint):
    _point_id = SetAmountApprovedID()
    _create_contract = SetAmountApprovedContract

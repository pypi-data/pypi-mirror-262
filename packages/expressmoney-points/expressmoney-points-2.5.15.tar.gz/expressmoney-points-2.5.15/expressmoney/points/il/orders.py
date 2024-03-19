__all__ = ('OrderPoint', 'OrderObjectPoint', 'SchedulePoint', 'ResendSmsSignPoint')

from expressmoney.api import *

SERVICE = 'il'


class OrderCreateContract(Contract):
    requested_amount = serializers.IntegerField(min_value=1)
    requested_period = serializers.IntegerField(min_value=1)
    bank_card_id = serializers.IntegerField(min_value=1)


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
    approved_amount = serializers.DecimalField(max_digits=7, decimal_places=0, allow_null=True)
    approved_period = serializers.IntegerField(min_value=1)
    product = serializers.IntegerField()
    status = serializers.ChoiceField(choices=STATUS_CHOICES)
    contract_demo = serializers.CharField(max_length=256, allow_blank=True)


class ScheduleReadContract(Contract):
    id = serializers.IntegerField()
    order = serializers.IntegerField()
    payments_number = serializers.IntegerField()
    date = serializers.DateField()
    amount = serializers.DecimalField(max_digits=7, decimal_places=0)
    amount_total = serializers.DecimalField(max_digits=7, decimal_places=0)
    amount_interests = serializers.DecimalField(max_digits=7, decimal_places=0)
    amount_body = serializers.DecimalField(max_digits=7, decimal_places=0)
    body_left_to_pay = serializers.DecimalField(max_digits=7, decimal_places=0)
    is_paid = serializers.BooleanField()


class ResendSmsSignCreateContract(Contract):
    pass


class OrderID(ID):
    _service = SERVICE
    _app = 'orders'
    _view_set = 'order'


class ScheduleID(ID):
    _service = SERVICE
    _app = 'orders'
    _view_set = 'schedule'


class ResendSmsSignPointID(ID):
    _service = SERVICE
    _app = 'orders'
    _view_set = 'resend_sms_sign'


class OrderPoint(ListPointMixin, CreatePointMixin, ContractPoint):
    _point_id = OrderID()
    _read_contract = OrderReadContract
    _create_contract = OrderCreateContract


class OrderObjectPoint(RetrievePointMixin, ContractObjectPoint):
    _point_id = OrderID()
    _read_contract = OrderReadContract


class SchedulePoint(ListPointMixin, ContractPoint):
    _point_id = ScheduleID()
    _read_contract = ScheduleReadContract


class ResendSmsSignPoint(CreatePointMixin, ContractPoint):
    _point_id = ResendSmsSignPointID()
    _create_contract = ResendSmsSignCreateContract

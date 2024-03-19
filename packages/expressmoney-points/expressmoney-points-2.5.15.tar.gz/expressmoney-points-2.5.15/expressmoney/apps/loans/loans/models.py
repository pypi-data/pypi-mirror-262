from decimal import Decimal

from django.db import models
from django.utils import timezone

from expressmoney.apps.loans.accounting.models import LoanIssueOperation, LoanBodyPaymentOperation, LoanInterestsOperation, \
    LoanInterestsPaymentOperation
from expressmoney.apps.loans.loans import utils


class Loan(models.Model):
    ISSUING = 'ISSUING'
    OPEN = "OPEN"  # Customer received money
    OVERDUE = "OVERDUE"
    STOP_INTEREST = "STOP_INTEREST"
    CLOSED = "CLOSED"
    CANCELED = 'CANCELED'
    STATUS_CHOICES = {
        (ISSUING, ISSUING),
        (OPEN, "Open"),
        (OVERDUE, "Overdue"),
        (STOP_INTEREST, "Stop interest"),
        (CLOSED, "Closed"),
        (CANCELED, CANCELED),
    }
    OPEN_STATUSES = (ISSUING, OPEN, OVERDUE, STOP_INTEREST)

    LOAN_BODY = 'LOAN_BODY'
    LOAN_INTERESTS = 'LOAN_INTERESTS'
    LOAN_ISSUE = 'LOAN_ISSUE'
    COMMON_PAYMENT = 'COMMON_PAYMENT'

    PAY_TYPE_CHOICES = {
        (LOAN_BODY, 'Pay body'),
        (LOAN_INTERESTS, 'Pay interests'),
        (LOAN_ISSUE, LOAN_ISSUE),
        (COMMON_PAYMENT, COMMON_PAYMENT),
    }

    created = models.DateTimeField('Создан', auto_now_add=True)
    updated = models.DateTimeField('Изменен', auto_now=True)
    extended_start_date = models.DateField('Начало пролонгации', null=True)
    extended_end_date = models.DateField('Конец пролонгации', null=True)
    order = models.OneToOneField('orders.Order', on_delete=models.CASCADE, verbose_name='Заявка')
    bank_card_id = models.PositiveIntegerField('Банковская карта', null=True)
    interests_charged_date = models.DateField('Проценты начислены', null=True)
    status = models.CharField('Статус', max_length=16, choices=STATUS_CHOICES, default=ISSUING)
    closed_date = models.DateTimeField('Дата закрытия', null=True)
    sign = models.PositiveSmallIntegerField('Цифровая подпись')
    ip = models.GenericIPAddressField()
    document = models.CharField('Печатный договор', max_length=256, blank=True)
    comment = models.CharField('Комментарий', max_length=2048, blank=True)

    def save(self, *args, **kwargs):
        pass

    @property
    def amount(self):
        if self.__amount is None:
            self.__amount = Decimal(self.order.amount_approved)
        return self.__amount

    @property
    def period(self):
        if self.__period is None:
            self.__period = self.order.period_approved
        return self.__period

    @property
    def free_period(self):
        if self.__free_period is None:
            self.__free_period = self.order.period_free
        return self.__free_period

    @property
    def interests(self):
        if self.__interests is None:
            self.__interests = self.order.interests
        return self.__interests

    @property
    def expiry_date(self):
        """Крайняя дата платежа по займу"""
        if self.__expiry_date is None:
            issue_date = self.created
            self.__expiry_date = issue_date.date() + timezone.timedelta(days=self.period) \
                if issue_date is not None else None
        if self.extended_end_date:
            self.__expiry_date = self.extended_end_date
        return self.__expiry_date

    @property
    def expiry_period(self):
        """На сколько дней просрочена оплата по займу"""
        if self.closed_date and self.status == self.CLOSED:
            expiry_period = (self.closed_date.date() - self.expiry_date).days
            self.__expiry_period = expiry_period if expiry_period >= 0 else 0
        if not self.closed_date and self.status == self.CLOSED:
            self.__expiry_period = None
        elif self.__expiry_period is None and self.expiry_date is not None:
            if self.extended_end_date:
                expiry_period = (timezone.now().date() - self.extended_end_date).days
            else:
                expiry_period = (timezone.now().date() - self.expiry_date).days
            self.__expiry_period = expiry_period if expiry_period >= 0 else 0
        return self.__expiry_period

    @property
    def body_issue(self):
        if self.__body_issue is None:
            obj = LoanIssueOperation.objects.filter(loan=self).order_by('created').last()
            if obj:
                self.__body_issue = obj.balance
            else:
                self.__body_issue = Decimal(0)
        return self.__body_issue

    @property
    def body_balance(self):
        return self.body_issue - self.body_paid

    @property
    def body_paid(self):
        if self.__body_paid is None:
            obj = LoanBodyPaymentOperation.objects.filter(loan=self).order_by('created').last()
            if obj:
                self.__body_paid = obj.balance
            else:
                self.__body_paid = Decimal(0)
        return self.__body_paid

    @property
    def interests_total(self):
        """Total loan interests charged"""
        if self.__interests_total is None:
            obj = LoanInterestsOperation.objects.filter(loan=self).order_by('created').last()
            if obj:
                self.__interests_total = obj.balance
            else:
                self.__interests_total = Decimal(0)
        return self.__interests_total

    @property
    def interests_paid(self):
        if self.__interests_paid is None:
            obj = LoanInterestsPaymentOperation.objects.filter(loan=self).order_by('created').last()
            if obj:
                self.__interests_paid = obj.balance
            else:
                self.__interests_paid = Decimal(0)
        return self.__interests_paid

    @property
    def interests_balance(self):
        if self.is_first_day_payment and self.interests_total == 0:
            interest_calculator = utils.InterestsCalculator(self)
            interests = interest_calculator._interest
            if interests != 0:
                return self.order.amount_approved / 100 * self.interests
            return Decimal(0)
        return self.interests_total - self.interests_paid

    @property
    def is_today_paid_interests(self):
        return LoanInterestsPaymentOperation.objects.\
            filter(loan_id=self.id, created__gte=timezone.now().date()).exists()

    @property
    def bank_card(self):
        return self.order.bank_card_id

    @property
    def is_first_day_payment(self):
        return self.created.date() == timezone.now().date()

    def _set_attrs(self):
        self.__balance_body = None
        self.__body_issue = None
        self.__body_paid = None
        self.__interests_total = None
        self.__interests_paid = None
        self.__balance_interest = None
        self.__expiry_date = None
        self.__expiry_period = None
        self.__period = None
        self.__free_period = None
        self.__interests = None
        self.__amount = None
        self.__user = None
        self.__extended_period = None
        self.__extended_date = None
        self.__active_restructure = None

    def __init__(self, *args, **kwargs):
        self._set_attrs()
        super().__init__(*args, **kwargs)

    def __str__(self):
        return f'Loan {self.id}'

    class Meta:
        managed = False
        verbose_name = 'Займ'
        verbose_name_plural = 'Займы'

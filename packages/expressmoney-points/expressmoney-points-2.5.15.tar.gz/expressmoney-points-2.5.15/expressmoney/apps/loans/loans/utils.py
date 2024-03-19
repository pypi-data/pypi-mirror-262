from decimal import Decimal

from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class InterestLimit(Exception):
    pass


class InterestExists(Exception):
    pass


class InterestsCalculator:

    def __init__(self, loan):
        self.__charge_interest_balance = None
        self.__interest_calculate_date = None
        self.__interest_limit = None
        self.__interest = None
        self._loan = loan

    def calculate(self) -> Decimal:
        if self._check_prohibition_before_calculation():
            raise InterestExists
        if self._loan.is_first_day_payment:
            calculate_interest = int((self._loan.order.amount_approved / 100) * self._interest)
        else:
            calculate_interest = int((self._loan.body_balance / 100) * self._interest)
        # Если начисляемый процент + общая сумма начисленных процентов по этому займу больше его лимита
        if self._charge_interest_balance + calculate_interest > self._interest_limit:
            # то начисляемый процент будет ровно столько, сколько не хватает до лимита
            calculate_interest = self._interest_limit - self._charge_interest_balance

        return Decimal(calculate_interest)

    @property
    def _interest_calculate_date(self):
        """Дата, на которую требуется расчет процентного дохода в текущий момент."""
        return timezone.localdate()

    @property
    def _charge_interest_balance(self):
        """Получить общую сумму начисленных процентов на клиента по текущему займу"""
        if self.__charge_interest_balance is None:
            self.__charge_interest_balance = self._loan.interests_total
        return self.__charge_interest_balance

    @property
    def _interest_limit(self):
        """Получить лимит начисленных процентов"""
        if self.__interest_limit is None:
            # Фактическая сумма первоначального займа
            loan_amount = int(self._loan.amount)
            # Лимит начисляемых % не должна превышать 130% от суммы первоначального займа
            interest_limit = int(loan_amount * 1.3)
            # Если общая сумма начисленных % по этому займу уже достиг лимит, то это остановка начисления %
            if self._charge_interest_balance >= interest_limit:
                raise InterestLimit
            else:
                self.__interest_limit = interest_limit
        return self.__interest_limit

    @property
    def _interest(self) -> Decimal:
        """
        Процентная ставка.
        Беспроцентный период - это последние дни пользования займом, учитывается только самый первый срок пользования.
        Беспроцентный период был сдвинут на 1 день назад, в последний день процент должен быть начислен, иначе
        мы не сможем начислять проценты с момента просрочки до полуторакратного размера (1,5 х).
        """
        if self.__interest is None:
            interest = (self._loan.interests
                        if self._loan.created.date() > timezone.datetime.fromisoformat('2023-06-30').date() else 1)
            loan_date = self._loan.created.date()
            loan_period = self._loan.period
            loan_interest_free_period = self._loan.free_period
            # Дата начала беспроцентного периода. Включительно.
            date_start_interest_free_period = (
                    loan_date + timezone.timedelta(days=loan_period - loan_interest_free_period - 1))
            # Дата окончания беспроцентного периода. Включительно.
            date_end_interest_free_period = (loan_date + timezone.timedelta(days=loan_period - 1))
            # Если беспроцентный период присутствует, то проверяем его. Если его нет, то пропускаем проверку
            if loan_interest_free_period > 0 and \
                    date_start_interest_free_period <= self._interest_calculate_date \
                    <= date_end_interest_free_period:
                self.__interest = 0
            else:
                self.__interest = interest
        return self.__interest

    def _check_prohibition_before_calculation(self):
        """Проверить, запрещено ли делать расчёт процентного дохода по займу в текущий момент"""
        loan_body_balance = int(self._loan.body_balance)
        interests_charged_date = self._loan.interests_charged_date
        if interests_charged_date is not None and \
                (self._interest_calculate_date <= interests_charged_date or loan_body_balance == 0):
            return True
        # Если проценты уже были, дата начисления != дате последнего начисления и остаток != 0, то начислять % можно
        else:
            return False

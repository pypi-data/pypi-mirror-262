from django.db import models, transaction


class OperationAbstract(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    loan = models.ForeignKey('loans.Loan', models.CASCADE, related_name="%(class)s")
    amount = models.DecimalField(max_digits=16, decimal_places=0)
    balance = models.DecimalField(max_digits=16, decimal_places=0)
    payment_id = models.PositiveIntegerField(default=0, null=True)

    @transaction.atomic
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.id is None:
            from loans.models import Loan
            self.loan = Loan.objects.select_for_update().get(id=self.loan.id)
            self._set_balance()
            super().save(force_insert, force_update, using, update_fields)
            transaction.on_commit(self._do_after_commit)

    def _set_balance(self):
        last_obj = self.__class__.objects.filter(loan=self.loan).last()
        self.balance = last_obj.balance if last_obj is not None else 0
        self.balance += self.amount

    def _do_after_commit(self):
        pass

    class Meta:
        abstract = True


class LoanIssueOperation(OperationAbstract):
    pass

    class Meta:
        managed = False
        verbose_name = 'Выдачи'
        verbose_name_plural = 'Выдачи'


class LoanInterestsOperation(OperationAbstract):
    class Meta:
        managed = False
        verbose_name = 'Начисленные проценты'
        verbose_name_plural = 'Начисленные проценты'


class LoanInterestsPaymentOperation(OperationAbstract):
    bank_card_id = models.PositiveIntegerField(null=True)

    class Meta:
        managed = False
        verbose_name = 'Выплаченные проценты'
        verbose_name_plural = 'Выплаченные проценты'


class LoanBodyPaymentOperation(OperationAbstract):
    bank_card_id = models.PositiveIntegerField(null=True)

    class Meta:
        managed = False
        verbose_name = 'Выплаченное тело'
        verbose_name_plural = 'Выплаченное тело'

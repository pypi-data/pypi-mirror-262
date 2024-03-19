from django.db import models


class Order(models.Model):
    NEW = 'NEW'
    DECLINED = 'DECLINED'
    LOAN_CREATED = 'LOAN_CREATED'
    EXPIRED = 'EXPIRED'
    STATUS_CHOICES = (
        (NEW, 'Новая'),
        (DECLINED, 'Отклонена'),
        (LOAN_CREATED, 'Займ создан'),
        (EXPIRED, 'Истекла'),
    )

    created = models.DateTimeField('Создана', auto_now_add=True)
    updated = models.DateTimeField('Обновлена', auto_now=True)
    user_id = models.PositiveIntegerField('Клиент')
    amount_requested = models.DecimalField('Запрошенная сумма', max_digits=7, decimal_places=0)
    amount_approved = models.DecimalField('Одобренная сумма', max_digits=7, decimal_places=0, null=True)
    period_requested = models.PositiveSmallIntegerField('Запрошенный период')
    period_approved = models.PositiveSmallIntegerField('Одобренный период', blank=True, null=True)
    period_free = models.PositiveSmallIntegerField('Беспроцентный период', default=0)
    interests = models.DecimalField('Процентная ставка', max_digits=3, decimal_places=2)
    status = models.CharField('Статус', max_length=30, choices=STATUS_CHOICES, default=NEW)
    promocode_code = models.CharField('Промокод', max_length=16, blank=True)
    is_first_loan = models.BooleanField('Первый займ', null=True, blank=True)
    is_first_order = models.BooleanField('Первая заявка', null=True, blank=True)
    department_id = models.PositiveIntegerField('Бизнес-юнит', null=True)

    def __str__(self):
        return f'{self.pk}'

    class Meta:
        managed = False
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

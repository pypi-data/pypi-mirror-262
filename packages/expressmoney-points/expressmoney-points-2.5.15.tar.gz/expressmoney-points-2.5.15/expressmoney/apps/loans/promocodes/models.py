from django.db import models
from django.utils import timezone


class PromocodeDescription(models.Model):
    created = models.DateTimeField('Создан', auto_now_add=True)
    updated = models.DateTimeField('Изменен', auto_now=True)
    code = models.CharField('Код', max_length=4, unique=True)
    product = models.ForeignKey('products.Product', models.CASCADE)
    valid_from = models.DateField(help_text='Дата начала действия купона')
    valid_to = models.DateField(help_text='Дата окончания действия купона')
    total = models.PositiveIntegerField(help_text='Всего купонов')
    activated = models.PositiveIntegerField(help_text='Активировано', default=0)
    comment = models.CharField(max_length=64, blank=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self._transform_code()
        super().save(force_insert, force_update, using, update_fields)

    @property
    def is_active(self):
        today = timezone.now().date()
        return self.valid_to >= today >= self.valid_from and self.total > self.activated

    def activate(self):
        if self.is_active:
            self.activated += 1
            super().save()

    def _transform_code(self):
        self.code = self.code.upper()

    def __str__(self):
        return self.code

    class Meta:
        managed = False
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'


class PromoCode(models.Model):
    created = models.DateTimeField('Активирован', auto_now_add=True)
    code = models.CharField('Промокод', max_length=8)
    user_id = models.PositiveIntegerField('Клиент')
    promocode_description = models.ForeignKey('PromocodeDescription', models.PROTECT, verbose_name='Описание промокода')

    def save(self, *args, **kwargs):
        pass

    class Meta:
        managed = False
        verbose_name = 'Активированный промокод'
        verbose_name_plural = 'Активированные промокоды'

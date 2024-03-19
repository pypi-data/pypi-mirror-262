from django.db import models


class Product(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    free_period = models.PositiveSmallIntegerField(default=0)
    interests = models.DecimalField(max_digits=3, decimal_places=2, default=1)

    def __str__(self):
        return f'{self.free_period}_{str(self.interests)}'

    class Meta:
        managed = False
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

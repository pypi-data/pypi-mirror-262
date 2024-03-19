from django.db import models
from expressmoney.points.loans import BlackListPoint


class BlackList(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user_id = models.PositiveIntegerField(primary_key=True)
    comment = models.CharField(max_length=128, blank=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        BlackListPoint(self.user_id).flush_cache()

    class Meta:
        managed = False
        verbose_name = 'Черный список'
        verbose_name_plural = 'Черный список'

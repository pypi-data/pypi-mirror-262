from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


alphanumeric = RegexValidator(r'^[0-9a-zA-Z_-а-яА-Я]*$', 'Only alphanumeric characters are allowed.')


class FileType(models.Model):
    type = models.CharField(max_length=32, unique=True, validators=(alphanumeric,))
    extensions = models.CharField(max_length=128, help_text=_('Examples 1: pdf 2: jpg,gif,png'))
    comment = models.CharField(max_length=128)

    def __str__(self):
        return self.type

    class Meta:
        managed = False


class File(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user_id = models.PositiveIntegerField(null=True)
    name = models.CharField(max_length=64, unique=True, validators=(alphanumeric,))
    type = models.ForeignKey('FileType', models.CASCADE)
    is_public = models.BooleanField(default=False)
    file = models.FileField()
    underwriter_id = models.PositiveIntegerField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'

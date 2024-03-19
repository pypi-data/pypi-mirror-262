from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from expressmoney.django.mixins import ModelDiffMixin
from expressmoney.points.profiles import UserProfileObjectPoint
from phonenumber_field.modelfields import PhoneNumberField

User = get_user_model()


class UserProfile(models.Model):
    user_id = models.PositiveIntegerField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    department = models.ForeignKey('Department', models.CASCADE)
    country = models.CharField(max_length=4, )
    ip = models.GenericIPAddressField()
    http_referer = models.URLField(blank=True, max_length=2048)

    @property
    def user(self):
        if self.__user is None:
            self.__user = User.objects.get(id=self.user_id)
        return self.__user

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self._flush_cache()
        super().save(force_insert, force_update, using, update_fields)

    def _flush_cache(self):
        UserProfileObjectPoint(self.user, self.user_id).flush_cache()

    def _set_attrs(self):
        self.__user = None

    def __init__(self, *args, **kwargs):
        self._set_attrs()
        super().__init__(*args, **kwargs)

    def __str__(self):
        return str(self.user_id)

    class Meta:
        managed = False


class Department(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=64)
    parent = models.ForeignKey('self', models.SET_NULL, blank=True, null=True)
    comment = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return self.name


class AbstractProfile(models.Model):
    NONE = 'NONE'
    PASSPORT = "PP"
    DRIVING_LICENCE = "DL"
    INSURANCE = "INSURANCE"
    TAX_ID = "TAX_ID"
    GOVERNMENT_ID_TYPE_CHOICES = (
        (NONE, 'None'),
        (PASSPORT, "Passport"),
        (DRIVING_LICENCE, "Driving licence"),
        (TAX_ID, "Tax ID"),
        (INSURANCE, 'SNILS'),
    )

    # Common data
    user_profile = models.OneToOneField('UserProfile', models.CASCADE, primary_key=True)
    created = models.DateTimeField('Создать', auto_now_add=True)
    updated = models.DateTimeField('Изменен', auto_now=True)
    first_name = models.CharField('Имя', max_length=32)
    last_name = models.CharField('Фамилия', max_length=32)
    middle_name = models.CharField('Отчество', max_length=32)
    birth_date = models.DateField('Дата рождения')
    birth_place = models.CharField(max_length=256, blank=True)
    # Phonenumbers
    tel_1 = PhoneNumberField('Тел 1', blank=True)
    tel_2 = PhoneNumberField('Тел 2', blank=True)
    tel_3 = PhoneNumberField('Тел 3', blank=True)
    tel_4 = PhoneNumberField('Тел 4', blank=True)
    tel_5 = PhoneNumberField('Тел 5', blank=True)
    # Underwriting
    is_identified = models.BooleanField('Идентифицирован', default=False)
    is_verified = models.BooleanField('Верифицирован', default=False)
    is_verified_date = models.DateField('Дата верификации', null=True)
    sign_date = models.DateField('Личный подпись', null=True)
    credit_score = models.DecimalField('Кредитный рейтинг', max_digits=3, decimal_places=2, null=True, blank=True)
    credit_score_created = models.DateTimeField('Дата кредитного рейтинга', null=True, blank=True)
    is_read_only = models.BooleanField(default=False)
    # Address
    postal_code = models.CharField('Почтовый индекс', max_length=16, blank=True)
    state = models.CharField('Регион', max_length=256, blank=True, help_text='required')
    city = models.CharField('Город', max_length=256, blank=True, help_text='required')
    street = models.CharField('Улица', max_length=256, blank=True, help_text='required')
    street_house = models.CharField('Дом', max_length=8, blank=True, help_text='required')
    street_building = models.CharField(max_length=4, blank=True)
    street_lane = models.CharField(max_length=16, blank=True)
    street_apartment = models.CharField('Квартира', max_length=8, blank=True, help_text='required')
    address = models.CharField('Полный адрес', max_length=256, blank=True, help_text=_('address in line'))
    address_optional = models.CharField(max_length=64, blank=True)
    po_box = models.CharField(max_length=8, blank=True)
    address_code = models.CharField(max_length=64, blank=True, help_text='Example KLADR')
    address_coordinates = models.CharField(max_length=64, blank=True)
    # Government ID
    government_id_type = models.CharField(max_length=32, choices=GOVERNMENT_ID_TYPE_CHOICES, default=NONE)
    government_id_number = models.CharField(max_length=16, help_text=_('number of government id'), blank=True)
    government_id_date = models.DateField(help_text=_('issue or expired date of government id'), null=True, blank=True)

    @property
    def user(self):
        if self.__user is None:
            self.__user = User.objects.get(id=self.user_profile.user_id)
        return self.__user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__user = None

    class Meta:
        abstract = True


class Profile(ModelDiffMixin, AbstractProfile):
    def __str__(self):
        return f'{self.user_profile_id}'

    class Meta:
        managed = False
        unique_together = ('first_name', 'last_name', 'middle_name', 'birth_date')


class RussianProfile(Profile):
    passport_serial = models.CharField('Серия паспорта', max_length=4)
    passport_number = models.CharField('Номер паспорта', max_length=6)
    passport_issue_name = models.CharField('Кем выдан', max_length=256)
    passport_code = models.CharField('Код паспорта', max_length=16)
    passport_date = models.DateField('Дата выдачи', help_text=_('Date of issue'))
    income = models.PositiveIntegerField('Доход', blank=True, null=True)
    income_region = models.PositiveIntegerField('Регион дохода', blank=True, null=True)
    court_address = models.CharField(max_length=256, blank=True)
    fias_region = models.CharField(max_length=256, blank=True, help_text=_('FIAS region address'))
    snils = models.CharField('СНИЛС', max_length=64, null=True)

    class Meta:
        managed = False
        unique_together = ('passport_serial', 'passport_number')
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

__all__ = ('UserProfilePoint', 'UserProfileObjectPoint', 'RussianProfilePoint', 'RussianProfileObjectPoint',
           'ProfileObjectPoint', 'UserProfileIpExistsPoint', 'UnlimitedSetCreditScorePoint', 'DocumentPoint',
           'SendSignPoint', 'ValidateSignPoint', 'AgreementPoint', 'RussianPersonalAgreementPoint',
           'SetCreditScorePoint', 'UpdateClientAddressPoint', 'SetIsVerifiedPoint')

from expressmoney.api import *

SERVICE = 'profiles'


class UserProfileCreateContract(Contract):
    user_id = serializers.IntegerField(min_value=1)
    department = serializers.IntegerField(min_value=1)
    ip = serializers.IPAddressField()
    http_referer = serializers.URLField(allow_blank=True, max_length=2048)


class UserProfileReadContract(UserProfileCreateContract):
    created = serializers.DateTimeField()
    country = serializers.CharField(max_length=2)
    ip = serializers.IPAddressField()


class SetIsVerifiedCreateContract(Contract):
    is_verified = serializers.BooleanField(allow_null=True)


class ProfileUpdateContract(Contract):
    first_name = serializers.CharField(max_length=32)
    last_name = serializers.CharField(max_length=32)
    middle_name = serializers.CharField(max_length=32)
    birth_date = serializers.DateField()
    state = serializers.CharField(max_length=256, allow_blank=True)
    city = serializers.CharField(max_length=256, allow_blank=True)
    street = serializers.CharField(max_length=256, allow_blank=True)
    street_house = serializers.CharField(max_length=8, allow_blank=True)
    street_apartment = serializers.CharField(max_length=8, allow_blank=True)
    address = serializers.CharField(max_length=256, allow_blank=True)


class ProfileCreateContract(ProfileUpdateContract):
    NONE = 'NONE'
    PASSPORT = "PP"
    DRIVING_LICENCE = "DL"
    INSURANCE = "INSURANCE"
    TAX_ID = "TAX_ID"
    GOVERNMENT_ID_TYPE_CHOICES = (
        (NONE, gettext_lazy('None')),
        (PASSPORT, gettext_lazy("Passport")),
        (DRIVING_LICENCE, gettext_lazy("Driving licence")),
        (TAX_ID, gettext_lazy("Tax ID")),
        (INSURANCE, gettext_lazy('SNILS')),
    )
    # Address
    postal_code = serializers.CharField(max_length=16, allow_blank=True)
    state = serializers.CharField(max_length=256, allow_blank=True)
    city = serializers.CharField(max_length=256, allow_blank=True)
    street = serializers.CharField(max_length=256, allow_blank=True)
    street_house = serializers.CharField(max_length=8, allow_blank=True)
    street_building = serializers.CharField(max_length=4, allow_blank=True)
    street_lane = serializers.CharField(max_length=16, allow_blank=True)
    street_apartment = serializers.CharField(max_length=8, allow_blank=True)
    address = serializers.CharField(max_length=256, allow_blank=True)
    address_optional = serializers.CharField(max_length=64, allow_blank=True)
    po_box = serializers.CharField(max_length=8, allow_blank=True)
    # Government ID
    government_id_type = serializers.ChoiceField(choices=GOVERNMENT_ID_TYPE_CHOICES, default=NONE)
    government_id_number = serializers.CharField(max_length=16, allow_blank=True)
    government_id_date = serializers.DateField(allow_null=True, required=False)


class ProfileReadContract(ProfileCreateContract):
    created = serializers.DateTimeField()
    updated = serializers.DateTimeField()
    # Underwriting
    is_identified = serializers.BooleanField()
    is_verified = serializers.BooleanField()
    sign_date = serializers.DateField(allow_null=True)
    credit_score = serializers.DecimalField(max_digits=3, decimal_places=2, allow_null=True)
    credit_score_created = serializers.DateTimeField(allow_null=True)
    # Address
    address_code = serializers.CharField(max_length=64, allow_blank=True)
    address_coordinates = serializers.CharField(max_length=64, allow_blank=True)
    # property
    is_default = serializers.BooleanField(allow_null=True)


class RussianProfileUpdateContract(ProfileUpdateContract):
    passport_serial = serializers.CharField(max_length=4)
    passport_number = serializers.CharField(max_length=6)
    passport_code = serializers.CharField(max_length=16)
    passport_date = serializers.DateField()
    snils = serializers.CharField(max_length=64)


class RussianProfileUpdateAddressContract(Contract):
    postal_code = serializers.CharField(max_length=16)
    state = serializers.CharField(max_length=256)
    city = serializers.CharField(max_length=256)
    street = serializers.CharField(max_length=256)
    street_house = serializers.CharField(max_length=8)
    street_apartment = serializers.CharField(max_length=8, allow_blank=True)
    address = serializers.CharField(max_length=256)
    fias_region = serializers.CharField(max_length=256)


class RussianProfileCreateContract(ProfileCreateContract):
    passport_serial = serializers.CharField(max_length=4)
    passport_number = serializers.CharField(max_length=6)
    passport_issue_name = serializers.CharField(max_length=256, allow_blank=True)
    passport_code = serializers.CharField(max_length=16)
    passport_date = serializers.DateField()
    income = serializers.IntegerField(allow_null=True, required=False)
    snils = serializers.CharField(max_length=64, allow_null=True, allow_blank=True)


class RussianProfileReadContract(ProfileReadContract):
    passport_serial = serializers.CharField(max_length=4)
    passport_number = serializers.CharField(max_length=6)
    passport_issue_name = serializers.CharField(max_length=256, allow_blank=True)
    passport_code = serializers.CharField(max_length=16)
    passport_date = serializers.DateField()
    income = serializers.IntegerField(allow_null=True)
    income_region = serializers.IntegerField(allow_null=True)
    court_address = serializers.CharField(max_length=256, allow_blank=True)
    fias_region = serializers.CharField(max_length=256, allow_blank=True)
    snils = serializers.CharField(max_length=64, allow_null=True, allow_blank=True)


class SignReadContract(Contract):
    sign = serializers.CharField(max_length=4)


class DocumentCreateContract(Contract):
    document = serializers.CharField(max_length=128)


class DocumentReadContract(Contract):
    created = serializers.DateTimeField()
    document = serializers.CharField(max_length=128)


class UserProfileIpExistsCreateContract(Contract):
    ip = serializers.IPAddressField()


class UserProfileIpExistsResponseContract(Contract):
    is_exist = serializers.BooleanField()


class SetCreditScoreCreateContract(Contract):
    pass


class LogCreateContract(Contract):
    full_name = serializers.CharField(max_length=64, allow_null=True)
    document = serializers.CharField(max_length=64, allow_null=True)
    address = serializers.CharField(max_length=64, allow_null=True)


class SendSignCreateContract(Contract):
    pass


class ValidateSignCreateContract(Contract):
    sign = serializers.CharField(max_length=4)


class ValidateSignResponseContract(Contract):
    is_valid = serializers.BooleanField()


class AgreementCreateContract(Contract):
    pass


class RussianPersonalAgreementCreateContract(Contract):
    sign = serializers.CharField(max_length=4, required=False)


class RussianProfileID(ID):
    _service = SERVICE
    _app = 'profiles'
    _view_set = 'russian_profile'


class RussianProfileUpdateAddressID(ID):
    _service = SERVICE
    _app = 'profiles'
    _view_set = 'update_client_address'


class UserProfileID(ID):
    _service = SERVICE
    _app = 'profiles'
    _view_set = 'user_profile'


class ProfileID(ID):
    _service = SERVICE
    _app = 'profiles'
    _view_set = 'profile'


class UserProfileIpExistsID(ID):
    _service = SERVICE
    _app = 'profiles'
    _view_set = 'user_profile_ip_exists'


class SetCreditScoreID(ID):
    _service = SERVICE
    _app = 'profiles'
    _view_set = 'set_credit_score'


class UnlimitedSetCreditScoreID(ID):
    _service = SERVICE
    _app = 'profiles'
    _view_set = 'unlimited_set_credit_score'


class LogID(ID):
    _service = SERVICE
    _app = 'profiles'
    _view_set = 'log'


class DocumentID(ID):
    _service = SERVICE
    _app = 'profiles'
    _view_set = 'document'


class SendSignID(ID):
    _service = SERVICE
    _app = 'profiles'
    _view_set = 'send_sign'


class SignID(ID):
    _service = SERVICE
    _app = 'profiles'
    _view_set = 'sign'


class ValidateSignID(ID):
    _service = SERVICE
    _app = 'profiles'
    _view_set = 'validate_sign'


class AgreementID(ID):
    _service = SERVICE
    _app = 'profiles'
    _view_set = 'agreement'


class RussianPersonalAgreementID(ID):
    _service = SERVICE
    _app = 'profiles'
    _view_set = 'russian_agreement'


class SetIsVerifiedID(ID):
    _service = SERVICE
    _app = 'profiles'
    _view_set = 'set_is_verified'


class UserProfilePoint(CreatePointMixin, ContractPoint):
    _point_id = UserProfileID()
    _create_contract = UserProfileCreateContract


class UserProfileObjectPoint(RetrievePointMixin, ContractObjectPoint):
    _point_id = UserProfileID()
    _read_contract = UserProfileReadContract


class RussianProfilePoint(CreatePointMixin, ContractPoint):
    _point_id = RussianProfileID()
    _create_contract = RussianProfileCreateContract


class RussianProfileObjectPoint(RetrievePointMixin, UpdatePointMixin, ContractObjectPoint):
    _point_id = RussianProfileID()
    _read_contract = RussianProfileReadContract
    _update_contract = RussianProfileUpdateContract


class UpdateClientAddressPoint(CreatePointMixin, ContractPoint):
    _point_id = RussianProfileUpdateAddressID()
    _create_contract = RussianProfileUpdateAddressContract


class ProfileObjectPoint(RetrievePointMixin, ContractObjectPoint):
    _point_id = ProfileID()
    _read_contract = ProfileReadContract


class UserProfileIpExistsPoint(ResponseMixin, CreatePointMixin, ContractPoint):
    _point_id = UserProfileIpExistsID()
    _create_contract = UserProfileIpExistsCreateContract
    _response_contract = UserProfileIpExistsResponseContract


class SetCreditScorePoint(CreatePointMixin, ContractPoint):
    _point_id = SetCreditScoreID()
    _create_contract = SetCreditScoreCreateContract


class UnlimitedSetCreditScorePoint(CreatePointMixin, ContractPoint):
    _point_id = UnlimitedSetCreditScoreID()
    _create_contract = SetCreditScoreCreateContract


class LogPoint(CreatePointMixin, ContractPoint):
    _point_id = LogID()
    _create_contract = LogCreateContract


class DocumentPoint(ListPointMixin, CreatePointMixin, ContractPoint):
    _point_id = DocumentID()
    _create_contract = DocumentCreateContract
    _read_contract = DocumentReadContract
    _sort_by = 'created'


class SendSignPoint(CreatePointMixin, ContractPoint):
    _point_id = SendSignID()
    _create_contract = SendSignCreateContract


class ValidateSignPoint(ResponseMixin, CreatePointMixin, ContractPoint):
    _point_id = ValidateSignID()
    _create_contract = ValidateSignCreateContract
    _response_contract = ValidateSignResponseContract


class SignObjectPoint(RetrievePointMixin, ContractObjectPoint):
    _point_id = SignID()
    _read_contract = SignReadContract


class AgreementPoint(CreatePointMixin, ContractPoint):
    _point_id = AgreementID()
    _create_contract = AgreementCreateContract


class RussianPersonalAgreementPoint(CreatePointMixin, ContractPoint):
    _point_id = RussianPersonalAgreementID()
    _create_contract = RussianPersonalAgreementCreateContract


class SetIsVerifiedPoint(CreatePointMixin, ContractPoint):
    _point_id = SetIsVerifiedID()
    _create_contract = SetIsVerifiedCreateContract

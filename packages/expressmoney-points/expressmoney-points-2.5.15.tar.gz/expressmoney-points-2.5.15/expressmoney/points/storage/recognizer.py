__all__ = ('RussianPassportRecognizerPoint', 'RussianPassportRecognizerObjectPoint')

from expressmoney.api import *

SERVICE = 'storage'


class RussianPassportRecognizerCreateContract(Contract):
    file_name = serializers.CharField(max_length=64)


class RussianPassportRecognizerResponseContract(RussianPassportRecognizerCreateContract):
    first_name = serializers.CharField(max_length=32, allow_blank=True)
    last_name = serializers.CharField(max_length=32, allow_blank=True)
    middle_name = serializers.CharField(max_length=32, allow_blank=True)
    birth_date = serializers.DateField(allow_null=True)
    passport_serial = serializers.CharField(max_length=4, allow_blank=True)
    passport_number = serializers.CharField(max_length=6, allow_blank=True)
    passport_issue_name = serializers.CharField(max_length=256, allow_blank=True)
    passport_code = serializers.CharField(max_length=16, allow_blank=True)
    passport_date = serializers.DateField(allow_null=True)
    gender = serializers.CharField(max_length=16, allow_blank=True)
    birth_place = serializers.CharField(max_length=256, allow_blank=True)


class RussianPassportRecognizerReadContract(RussianPassportRecognizerResponseContract):
    pass


class RussianPassportRecognizerID(ID):
    _service = SERVICE
    _app = 'recognizer'
    _view_set = 'russian_passport_recognizer'


class RussianPassportRecognizerPoint(CreatePointMixin, ResponseMixin, ContractPoint):
    _point_id = RussianPassportRecognizerID()
    _create_contract = RussianPassportRecognizerCreateContract
    _response_contract = RussianPassportRecognizerResponseContract


class RussianPassportRecognizerObjectPoint(RetrievePointMixin, ContractObjectPoint):
    _point_id = RussianPassportRecognizerID()
    _read_contract = RussianPassportRecognizerReadContract

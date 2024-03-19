__all__ = ('UploadFilePoint', 'UserFileObjectPoint', 'UserFilePoint', 'UploadPassportPoint', 'UserFileListPoint',
           'UserFileNameListPoint', 'RecognizeTrialVersionPoint')

from django.core.validators import RegexValidator

from expressmoney.api import *

SERVICE = 'storage'


class UploadFileResponseContract(Contract):
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z_]*$', 'Only alphanumeric characters are allowed.')
    name = serializers.CharField(max_length=64, validators=(alphanumeric,))


class UploadPassportResponseContract(UploadFileResponseContract):
    ...


class UserFileReadContract(UploadFileResponseContract):
    id = serializers.IntegerField(min_value=1)
    public_url = serializers.URLField(allow_null=True)
    file = serializers.URLField()


class UserFileListReadContract(Contract):
    id = serializers.IntegerField(min_value=1)
    name = serializers.CharField(max_length=64)
    type = serializers.CharField(max_length=2)
    file = serializers.URLField()


class UserFileNameListReadContract(Contract):
    id = serializers.IntegerField(min_value=1)
    name = serializers.CharField(max_length=64)


class RecognizeTrialVersionResponseContract(Contract):
    data = serializers.JSONField()
    file = serializers.IntegerField(min_value=1)
    file_name = serializers.CharField(max_length=64)


class RecognizeTrialVersionCreateContract(Contract):
    file_name = serializers.CharField(max_length=64)


class UserFileID(ID):
    _service = SERVICE
    _app = 'storage'
    _view_set = 'user_file'


class UploadFileID(ID):
    _service = SERVICE
    _app = 'storage'
    _view_set = 'upload_file/'


class UploadPassportID(ID):
    _service = SERVICE
    _app = SERVICE
    _view_set = 'upload_passport/'


class RecognizeTrialVersionID(ID):
    _service = SERVICE
    _app = 'recognizer'
    _view_set = 'recognize_trial_version'


class UserFileObjectPoint(RetrievePointMixin, ContractObjectPoint):
    _cache_enabled = False
    _point_id = UserFileID()
    _read_contract = UserFileReadContract


class UploadFilePoint(UploadFilePointMixin, ResponseMixin, ContractPoint):
    _point_id = UploadFileID()
    _response_contract = UploadFileResponseContract
    _read_contract = None


class UploadPassportPoint(UploadFilePointMixin, ResponseMixin, ContractPoint):
    _point_id = UploadPassportID()
    _response_contract = UploadPassportResponseContract
    _read_contract = None


class UserFilePoint(ListPointMixin, ContractPoint):
    _cache_enabled = False
    _point_id = UserFileID()
    _read_contract = UserFileReadContract


class UserFileListPoint(ListPointMixin, ContractPoint):
    _cache_enabled = False
    _point_id = UserFileID()
    _read_contract = UserFileListReadContract


class UserFileNameListPoint(UserFileListPoint):
    _read_contract = UserFileNameListReadContract


class RecognizeTrialVersionPoint(CreatePointMixin, ResponseMixin, ContractPoint):
    _point_id = RecognizeTrialVersionID()
    _response_contract = RecognizeTrialVersionResponseContract
    _create_contract = RecognizeTrialVersionCreateContract

__all__ = ('PassportReaderPoint', 'IDReaderPassportPoint','IDReaderProfilePoint')

from ..api import *

_SERVICE = 'services'
_APP = 'id_reader'

EMPTY = 'EMPTY'
SUCCESS = 'SCS'
FAILURE = 'FAIL'

RESULT_CHOICES = (
    (EMPTY, EMPTY),
    (FAILURE, FAILURE),
    (SUCCESS, SUCCESS),
)


class PassportReaderCreateContract(Contract):
    file = serializers.FileField()


class PassportReaderResponseContract(Contract):
    result = serializers.ChoiceField(choices=RESULT_CHOICES)
    data = serializers.JSONField(allow_null=True)


class IDReaderProfileCreateContract(Contract):
    first_name = serializers.CharField(max_length=32)
    last_name = serializers.CharField(max_length=32)
    middle_name = serializers.CharField(max_length=32)
    birthdate = serializers.DateField()
    passport_serial = serializers.CharField(max_length=4)
    passport_number = serializers.CharField(max_length=6)
    passport_code = serializers.CharField(max_length=16)
    passport_date = serializers.DateField()


class _PassportReader(ID):
    _service = _SERVICE
    _app = _APP
    _view_set = 'passport_reader'


class _IDReaderPassport(ID):
    _service = _SERVICE
    _app = _APP
    _view_set = 'passport_reader_v2'


class _IDReaderProfile(ID):
    _service = _SERVICE
    _app = _APP
    _view_set = 'user_profile'


class PassportReaderPoint(UploadFilePointMixin, ResponseMixin, ContractPoint):
    _point_id = _PassportReader()
    _create_contract = PassportReaderCreateContract
    _response_contract = PassportReaderResponseContract


class IDReaderPassportPoint(PassportReaderPoint):
    _point_id = _IDReaderPassport()


class IDReaderProfilePoint(CreatePointMixin, ContractPoint):
    _point_id = _IDReaderProfile()
    _create_contract = IDReaderProfileCreateContract

__all__ = ('TinkoffIDPoint',)

from phonenumber_field.serializerfields import PhoneNumberField

from expressmoney_service.api import *

_SERVICE = 'services'


class TinkoffIDCreateContract(Contract):
    code = serializers.CharField(max_length=32)


class TinkoffIDResponseContract(Contract):
    access_token = serializers.CharField(max_length=128)
    refresh_token = serializers.CharField(max_length=512)
    confirm_phone = serializers.BooleanField(default=False)
    first_name = serializers.CharField(max_length=32)
    last_name = serializers.CharField(max_length=32)
    middle_name = serializers.CharField(max_length=32)
    phone_number = PhoneNumberField()


class TinkoffID_ID(ID):
    _service = _SERVICE
    _app = 'tinkoff_id'
    _view_set = 'tinkoff_id'


class TinkoffIDPoint(CreatePointMixin, ResponseMixin, ContractPoint):
    _point_id = TinkoffID_ID()
    _create_contract = TinkoffIDCreateContract
    _response_contract = TinkoffIDResponseContract

__all__ = ('ConfirmationCodePoint',)

from expressmoney_service.api import *

_SERVICE = 'services'


class ConfirmationCodeId(ID):
    _service = _SERVICE
    _app = "megafon"
    _view_set = "confirmation"


class ConfirmationCodeCreateContract(Contract):
    confirmation_code = serializers.IntegerField()


class ConfirmationCodePoint(CreatePointMixin, ContractPoint):
    _point_id = ConfirmationCodeId()
    _create_contract = ConfirmationCodeCreateContract

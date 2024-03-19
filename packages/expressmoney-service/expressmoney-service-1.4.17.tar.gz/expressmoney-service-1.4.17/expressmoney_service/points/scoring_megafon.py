__all__ = ('ScoringMegafonPoint',)

from phonenumber_field.serializerfields import PhoneNumberField

from expressmoney_service.api import *

_SERVICE = 'services'


class ScoringMegafonCreateContract(Contract):
    phone_number = PhoneNumberField()


class ScoringMegafonResponseContract(Contract):
    score = serializers.FloatField()


class ScoringMegafonID(ID):
    _service = _SERVICE
    _app = 'scoring_megafon'
    _view_set = 'score'


class ScoringMegafonPoint(CreatePointMixin, ResponseMixin, ContractPoint):
    _point_id = ScoringMegafonID()
    _create_contract = ScoringMegafonCreateContract
    _response_contract = ScoringMegafonResponseContract

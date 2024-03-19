__all__ = ('AbsoluteInsurancePoint',)

from expressmoney_service.api import *


_SERVICE = 'services'
_APP = 'absolute_insurance'


class _AbsoluteInsuranceCreateContract(Contract):
    loan_id = serializers.IntegerField()
    body_balance = serializers.IntegerField()
    loan_created = serializers.DateField()
    loan_closing = serializers.DateField()
    option = serializers.CharField(max_length=32)
    phone_number = serializers.CharField(max_length=16)
    first_name = serializers.CharField(max_length=32)
    last_name = serializers.CharField(max_length=32)
    middle_name = serializers.CharField(max_length=32)
    birthdate = serializers.DateField()
    passport_serial = serializers.CharField(max_length=4)
    passport_number = serializers.CharField(max_length=6)
    passport_code = serializers.CharField(max_length=16)
    passport_date = serializers.DateField()
    fias_id = serializers.CharField(max_length=128, allow_blank=True)
    address = serializers.CharField(max_length=128, allow_blank=True)
    apartment = serializers.CharField(max_length=8, allow_blank=True)
    bin = serializers.CharField(max_length=6, allow_blank=True)
    number = serializers.CharField(max_length=4, allow_blank=True)
    expiry_month = serializers.CharField(max_length=2, allow_blank=True)
    expiry_year = serializers.CharField(max_length=2, allow_blank=True)
    sms_confirm = serializers.IntegerField(allow_null=True)


class _AbsoluteInsuranceResponseContract(Contract):
    insurance_contract = serializers.JSONField()


class _AbsoluteInsuranceID(ID):
    _service = _SERVICE
    _app = _APP
    _view_set = 'insurance_contract'


class AbsoluteInsurancePoint(CreatePointMixin, ResponseMixin, ContractPoint):
    _point_id = _AbsoluteInsuranceID()
    _create_contract = _AbsoluteInsuranceCreateContract
    _response_contract = _AbsoluteInsuranceResponseContract

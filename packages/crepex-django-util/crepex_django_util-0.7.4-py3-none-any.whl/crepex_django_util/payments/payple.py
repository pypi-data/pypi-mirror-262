from dataclasses import dataclass
from typing import Any
from typing import Optional
from typing import Callable

from django.test.signals import setting_changed
from rest_framework import serializers

from crepex_pyutil.exceptions import NotOkException
from crepex_pyutil.requests import AbstractRequestHelper
from ..settings import ModuleSettings
from ..settings import reload_settings_wrapper
from .types import PaymentType


@dataclass
class PaypleResult:

    ok: bool
    code: str
    message: str
    data: Any


@dataclass
class PaypleAuthResult:
    auth_key: str
    return_url: str
    cst_id: str
    cust_key: str


MODULE_SETTINGS_NAME = 'PAYPLE_SETTINGS'

DEFAULTS = {
    # Required
    'CST_ID': None,
    'CST_KEY': None,
    'REFUND_KEY': None,

    # Optional
    'DEMO': True,
    'SECURE': True,
}

module_settings = ModuleSettings(
    settings_name=MODULE_SETTINGS_NAME,
    defaults=DEFAULTS,
)

reload_settings = reload_settings_wrapper(module_settings)
setting_changed.connect(reload_settings)


class PayplePayment(
    AbstractRequestHelper,
):
    """
    페이플 결제모듈
    https://developer.payple.kr/
    """

    def __init__(self, logger: Optional[Callable[[str, Any], Any]] = None):
        super().__init__()
        self._init_session()
        self.payment_env = 'democpay' if module_settings.DEMO else 'cpay'
        self.api_url = f'https://{self.payment_env}.payple.kr'

        if logger:
            self.set_logger(logger)

    @staticmethod
    def get_referer(host: str):
        scheme = 'https' if module_settings.SECURE else 'http'
        return f'{scheme}://{host}'

    def get_result(self, data: Any) -> PaypleResult:
        ok = data['PCD_PAY_RST'] == 'success'
        if not ok:
            self.logging_response_error(f"{data['PCD_PAY_CODE']}_{data['PCD_PAY_MSG']}", data)
        return PaypleResult(
            ok=ok,
            code=data['PCD_PAY_CODE'],
            message=data['PCD_PAY_MSG'],
            data=data,
        )

    def authorize_partner(self, host: str, **kwargs):
        """
        파트너 인증
        """
        res = self.session.post(
            url=f'{self.api_url}/php/auth.php',
            headers=dict(
                Referer=self.get_referer(host),
            ),
            json=dict(
                cst_id=module_settings.CST_ID,
                custKey=module_settings.CST_KEY,
                **kwargs,
            ),
        )
        data = self.get_response_json(res, error_msg='파트너 인증실패')

        if data['result'] != 'success':
            self.logging_response_error(data['result_msg'], data)
            raise NotOkException(msg=data['result_msg'])

        return PaypleAuthResult(
            auth_key=data['AuthKey'],
            return_url=data['return_url'],
            cst_id=data['cst_id'],
            cust_key=data['custKey'],
        )

    def unregister_payment_method(self, host: str, key: str):
        """
        결제수단 등록해지
        https://developer.payple.kr/etc-api/registration-cancel
        """
        auth = self.authorize_partner(
            host=host,
            PCD_PAY_WORK='PUSERDEL',
        )
        res = self.session.post(
            url=auth.return_url,
            headers=dict(
                Referer=self.get_referer(host),
            ),
            json=dict(
                PCD_CST_ID=auth.cst_id,
                PCD_CUST_KEY=auth.cust_key,
                PCD_AUTH_KEY=auth.auth_key,
                PCD_PAYER_ID=key,
            ),
        )
        data = self.get_response_json(res, error_msg='결제수단 등록해제 실패')
        return self.get_result(data)

    def request_payment_from_billing_key(self, host: str, billing_key: str, order_id: str,
                                         payment_type: PaymentType, product_name: str,
                                         total: int, tax=0, **kwargs):
        """
        등록된 결제수단으로 결제요청
        """
        auth = self.authorize_partner(
            host=host,
            PCD_PAY_TYPE=payment_type.value,
            PCD_SIMPLE_FLAG='Y',
        )
        res = self.session.post(
            url=auth.return_url,
            headers=dict(
                Referer=self.get_referer(host),
            ),
            json=dict(
                PCD_CST_ID=auth.cst_id,
                PCD_CUST_KEY=auth.cust_key,
                PCD_AUTH_KEY=auth.auth_key,
                PCD_PAY_TYPE=payment_type.value,
                PCD_PAYER_ID=billing_key,
                PCD_PAY_GOODS=product_name,
                PCD_PAY_TOTAL=total,
                PCD_SIMPLE_FLAG='Y',
                PCD_PAY_OID=order_id,
                PCD_PAY_TAXTOTAL=tax,
                PCD_PAY_ISTAX='Y' if tax > 0 else 'N',
                **kwargs,
            ),
        )
        data = self.get_response_json(res, error_msg='등록 결제 실패')
        return self.get_result(data)

    def confirm_pay_simple(self, host: str, url: str, auth_key: str, req_key: str, payer_id: str):
        """
        일회성 결제 재컨펌
        """
        res = self.session.post(
            url=url,
            headers=dict(
                Referer=self.get_referer(host),
            ),
            json=dict(
                PCD_CST_ID=module_settings.CST_ID,
                PCD_CUST_KEY=module_settings.CST_KEY,
                PCD_AUTH_KEY=auth_key,
                PCD_PAY_REQKEY=req_key,
                PCD_PAYER_ID=payer_id,
            ),
        )
        data = self.get_response_json(res, error_msg='결제요청 컨펌 실패')
        return self.get_result(data)

    def cancel_payment(self, host, order_id: str, ordered_at: str, total: int, tax_total: Optional[int] = None):
        """
        결제 취소
        https://developer.payple.kr/etc-api/cancel-payment
        """
        auth = self.authorize_partner(
            host=host,
            PCD_PAYCANCEL_FLAG='Y',
        )

        data = dict(
            PCD_CST_ID=auth.cst_id,
            PCD_CUST_KEY=auth.cust_key,
            PCD_AUTH_KEY=auth.auth_key,
            PCD_REFUND_KEY=module_settings.REFUND_KEY,
            PCD_PAYCANCEL_FLAG='Y',
            PCD_PAY_OID=order_id,
            PCD_PAY_DATE=ordered_at,
            PCD_REFUND_TOTAL=total,
        )

        if tax_total:
            data['PCD_REFUND_TAXTOTAL'] = tax_total

        res = self.session.post(
            url=auth.return_url,
            headers=dict(
                Referer=self.get_referer(host),
            ),
            json=data,
        )
        data = self.get_response_json(res, error_msg='등록 결제 실패')
        return self.get_result(data)


class SimplePayConfirmDataSerializer(
    serializers.Serializer,
):
    """
    일회성 결제 컨펌 데이터
    https://developer.payple.kr/new/integration/simple-payment
    """

    cof_url = serializers.URLField()
    auth_key = serializers.CharField()
    req_key = serializers.CharField()
    payer_id = serializers.CharField()

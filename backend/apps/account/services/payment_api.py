import base64
import requests

from config.settings import PAYKEEPER_USER, PAYKEEPER_PASSWORD
from core.singleton import SingletonMeta


class PaykeeperPaymentApi(metaclass=SingletonMeta):
    _user = PAYKEEPER_USER
    _password = PAYKEEPER_PASSWORD
    _server_url = "https://tochka-chernogo.server.paykeeper.ru"

    def init_payment(self, payment):
        # Basic-авторизация передаётся как base64
        base64_auth = base64.b64encode(
            f"{self._user}:{self._password}".encode()
        ).decode()
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {base64_auth}",
        }

        # Параметры платежа, сумма - обязательный параметр
        # Остальные параметры можно не задавать
        payment_data = {
            "pay_amount": payment.price,
            "clientid": payment.user.username,
            "orderid": payment.uuid,
            "service_name": "Услуга",
        }

        # Запрос на получение токена безопасности
        token_uri = "/info/settings/token/"
        token_response = requests.get(f"{self._server_url}{token_uri}", headers=headers)

        if token_response.status_code == 200:
            token_data = token_response.json()
            token = token_data.get("token")
            if not token:
                raise ValueError("Ошибка: токен не получен.")
        else:
            raise ValueError(f"Ошибка получения токена: {token_response.text}")

        # Запрос на получение счёта
        invoice_uri = "/change/invoice/preview/"
        payment_data_with_token = {**payment_data, "token": token}

        invoice_response = requests.post(
            f"{self._server_url}{invoice_uri}",
            headers=headers,
            data=payment_data_with_token,
        )

        if invoice_response.status_code == 200:
            invoice_data = invoice_response.json()
            invoice_id = invoice_data.get("invoice_id")
            if not invoice_id:
                raise ValueError("Ошибка: invoice_id не получен.")
        else:
            raise ValueError(f"Ошибка получения счёта: {invoice_response.text}")

        # Прямая ссылка на оплату
        payment_url = f"{self._server_url}/bill/{invoice_id}/"
        return {"payment_url": payment_url}

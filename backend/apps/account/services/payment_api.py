import base64
import requests

from django.utils.timezone import localtime, timedelta
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

        # 15 минут на оплату
        expiry_datetime = localtime() + timedelta(minutes=15)

        # Параметры платежа, сумма - обязательный параметр
        # Остальные параметры можно не задавать
        payment_data = {
            "pay_amount": payment.price,
            "clientid": payment.user.username,
            "orderid": payment.uuid,
            "client_email": payment.email,
            "client_phone": str(payment.phone),
            "service_name": "Услуга",
            "expiry": expiry_datetime.strftime("%Y-%m-%d %H:%M:%S"),
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
        return {
            "invoice_id": invoice_id,
            "expiry_datetime": expiry_datetime,
            "payment_url": payment_url,
        }

    def get_payment_status(self, payment):
        base64_auth = base64.b64encode(
            f"{self._user}:{self._password}".encode()
        ).decode()

        # Заголовки для запроса
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {base64_auth}",
        }

        # Готовим запрос 3.1 JSON API на получение счёта
        uri = f"/info/invoice/byid/?id={payment.invoice_id}"
        url = f"{self._server_url}{uri}"

        # Выполняем запрос
        response = requests.get(url, headers=headers)

        # Проверяем статус ответа
        if response.status_code == 200:
            data = response.json()
            status = data.get("status")
            if status:
                print(f"Статус счёта: {status}")
            else:
                print("Ошибка: поле 'status' отсутствует в ответе.")
        else:
            print(f"Ошибка: {response.status_code}, {response.text}")

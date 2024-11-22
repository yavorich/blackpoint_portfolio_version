from requests import Session
from requests.models import PreparedRequest
from django.db.models import Model, EmailField, CharField
from config.settings import VENDISTA_API_URL
from core.builted.blank_and_null import blank_and_null

from .partner import Partner
from .place import Place


class VendistaAccount(Model):
    _server_url = VENDISTA_API_URL

    login = EmailField("Логин", unique=True)
    password = CharField("Пароль", max_length=32)

    token = CharField(max_length=32, **blank_and_null)

    class Meta:
        verbose_name = "аккаунт"
        verbose_name_plural = "Аккаунты Vendista"

    def get_auth_token(self):
        url = self._server_url + "/token"
        params = {"login": self.login, "password": self.password}

        request = PreparedRequest()
        request.prepare_url(url, params)

        session = Session()
        response = session.get(request.url)
        response_data = response.json()
        if response.status_code == 200:
            return response_data["token"]
        else:
            raise Exception("Ошибка получения токена: " + response_data["error"])

    def get_terminals(self):
        url = self._server_url + "/terminals"
        params = {"token": self.token, "ItemsOnPage": 100}

        request = PreparedRequest()
        session = Session()
        page = 1

        while True:
            params.update({"PageNumber": page})
            request.prepare_url(url, params)

            response = session.get(request.url)
            if response.status_code == 200:
                items = response.json()["items"]
                if len(items) == 0:
                    break
                self.sync_terminals_with_db(items)
            else:
                return
            page += 1

    def sync_terminals_with_db(self, items):
        partners, places = [], []
        for item in items:
            partner, created = Partner.objects.update_or_create(
                partner_id=item["owner_id"], defaults=dict(name=item["owner_name"])
            )
            place, created = Place.objects.update_or_create(
                terminal_id=item["id"],
                defaults=dict(
                    latitude=item["latitude"],
                    longitude=item["longitude"],
                    partner=partner,
                    vendista_account=self,
                ),
            )
            partners.append(partner)
            places.append(place)

        # TODO: get addresses

    def send_credits_to_terminal(self, terminal_id, num_credits):
        url = self._server_url + f"/terminals/{terminal_id}/commands"
        params = {"token": self.token}
        data = {"command_id": 20, "parameter1": num_credits * 100}

        request = PreparedRequest()
        request.prepare_url(url, params)

        session = Session()
        response = session.post(request.url, json=data)

        return response.status_code == 200

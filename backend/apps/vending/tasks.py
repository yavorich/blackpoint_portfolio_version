from celery import shared_task
from config.settings import VENDISTA_API_LOGIN, VENDISTA_API_PASSWORD, VENDISTA_API_URL
from requests import Session
from requests.models import PreparedRequest

# from geopy.geocoders import Nominatim

from apps.vending.models import Partner, Place


@shared_task
def add_credits_to_terminal(terminal_id, num_credits):
    token = get_auth_token()
    url = VENDISTA_API_URL + f"/terminals/{terminal_id}/commands"
    params = {"token": token}
    data = {"command_id": 20, "parameter1": num_credits}

    request = PreparedRequest()
    request.prepare_url(url, params)

    session = Session()
    response = session.post(request.url, json=data)
    response_data = response.json()
    if response.status_code == 200:
        return "Success"
    else:
        raise Exception("Ошибка отправки команды: ", response_data["error"])


@shared_task
def sync_places_with_api():
    token = get_auth_token()
    get_terminals(token)
    # geolocator = Nominatim(user_agent="tochka_chornogo_app")


def get_auth_token():
    url = VENDISTA_API_URL + "/token"
    params = {"login": VENDISTA_API_LOGIN, "password": VENDISTA_API_PASSWORD}

    request = PreparedRequest()
    request.prepare_url(url, params)

    session = Session()
    response = session.get(request.url)
    response_data = response.json()
    if response.status_code == 200:
        return response_data["token"]
    else:
        raise Exception("Ошибка получения токена: ", response_data["error"])


def get_terminals(token):
    url = VENDISTA_API_URL + "/terminals"
    params = {"token": token, "ItemsOnPage": 100}

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
            sync_terminals_with_db(items)
        else:
            return
        page += 1


def sync_terminals_with_db(items):
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
            ),
        )
        partners.append(partner)
        places.append(place)


# def set_terminal_address(place):
#     location = geolocator.reverse((latitude, longitude), language="ru")

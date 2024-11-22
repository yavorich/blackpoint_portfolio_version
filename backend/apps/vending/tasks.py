from celery import shared_task
import requests

from apps.vending.models import Place, City
from config.settings import YANDEX_GEOCODER_API_KEY


@shared_task
def set_all_terminal_addresses():
    places = Place.objects.filter(
        latitude__isnull=False, longitude__isnull=False, address__isnull=True
    )
    base_url = "https://geocode-maps.yandex.ru/1.x/?apikey={api_key}&geocode={lat},{lon}&format=json"
    for place in places:
        url = base_url.format(
            api_key=YANDEX_GEOCODER_API_KEY, lat=place.latitude, lon=place.longitude
        )
        response = requests.get(url)
        if not response.status_code == 200:
            return f"Не удалось получить адрес: status={response.status_code}"
        address_components = response.json()["response"]["GeoObjectCollection"][
            "featureMember"
        ][0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["Address"][
            "Components"
        ]
        city_name = None
        street = None
        house = None
        for component in address_components:
            if component["kind"] == "locality":
                city_name = component["name"]
            elif component["kind"] == "street":
                street = component["name"]
            elif component["kind"] == "house":
                house = component["name"]

        city, created = City.objects.get_or_create(name=city_name)
        address = f"{street}, {house}"

        place.city = city
        place.address = address
        place.save()
    return "Success"

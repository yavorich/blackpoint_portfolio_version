from os import path
import sys
from typing import Callable, Union


def get_upload_path(catalog, name_field, field) -> Union[str, Callable]:

    if len(sys.argv) > 1 and sys.argv[1] in ("makemigrations", "migrate"):
        return ""

    def upload_path(instance, filename) -> str:
        return path.join(
            catalog, str(getattr(instance, name_field)), f"{field}_{filename}"
        )

    return upload_path

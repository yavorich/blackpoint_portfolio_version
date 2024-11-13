from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import requests
from telegram import Update
from telegram.ext import CallbackContext


async def get_avatar(update: Update, context: CallbackContext) -> BytesIO | None:
    user = update.message.from_user

    user_photos = await context.bot.get_user_profile_photos(user_id=user.id)

    if user_photos.total_count > 0:
        # Берём самую большую фотографию
        photo_file = user_photos.photos[0][-1]  # Последний элемент - наибольший размер

        file_info = await context.bot.get_file(photo_file.file_id)

        response = requests.get(file_info.file_path)

        if response.status_code == 200:
            image_content = BytesIO(response.content)
            image_content.name = "avatar.jpg"

            return InMemoryUploadedFile(
                image_content,
                None,
                "avatar.jpg",
                "image/jpeg",
                image_content.getbuffer().nbytes,
                None,
            )
    else:
        return None

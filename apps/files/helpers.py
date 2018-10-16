import os

from multilibrary.settings import MEDIA_ROOT
from multilibrary.celery import app


@app.task
def is_exist_or_save_file(user_pk, file_path, user_file):
    folder_path = f'{MEDIA_ROOT}/{user_pk}'

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    with open(file_path, "wb") as new_image:
        for chunk in user_file.chunks():
            new_image.write(chunk)
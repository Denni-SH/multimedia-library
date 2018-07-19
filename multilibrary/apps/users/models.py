from django.contrib.auth.models import AbstractUser
from django.db.models import DateField, CharField, ImageField


class User(AbstractUser):
    avatar = ImageField(blank=True, default='default_user_avatar.jpeg')
    birth_date = DateField(null=True, blank=True)
    phone = CharField(max_length=20, blank=True)
    thumbnail = ImageField(blank=True, default='default_user_avatar.jpeg')

    def __str__(self):
        return self.username

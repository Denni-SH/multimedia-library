from django.contrib.auth.models import AbstractUser
from django.db.models import DateField, CharField, ImageField


class User(AbstractUser):
    avatar = ImageField(blank=True, default='default_user_avatar.jpeg')
    birth_date = DateField(null=True, blank=True, default=None)
    phone = CharField(max_length=20, blank=True, default=None, null=True)
    thumbnail = ImageField(blank=True, default='default_user_avatar.jpeg')

    @classmethod
    def create(cls, **kwargs):
        new_user = cls()
        new_user.avatar = kwargs.get('avatar') if kwargs.get('avatar') else None
        new_user.birth_date = kwargs.get('birth_date') if kwargs.get('birth_date') else None
        new_user.email = kwargs.get('email') if kwargs.get('email') else None
        new_user.first_name = kwargs.get('first_name') if kwargs.get('first_name') else None
        new_user.last_name = kwargs.get('last_name') if kwargs.get('last_name') else None
        new_user.password = kwargs.get('password')
        new_user.phone = kwargs.get('phone') if kwargs.get('phone') else None
        new_user.thumbnail = kwargs.get('thumbnail')
        new_user.username = kwargs.get('username')
        return new_user

    def __str__(self):
        return self.username if self.username else '%s %s' % (self.first_name, self.last_name)

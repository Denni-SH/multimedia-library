import uuid

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db.models import signals, DateField, CharField, ImageField, BooleanField, UUIDField, EmailField

from .tasks import send_verification_email


def user_directory_path(instance, filename):
    return f'{instance.pk}/{filename}'


class User(AbstractUser):
    avatar = ImageField(blank=True, default='default/default-user.jpg', upload_to=user_directory_path)
    birth_date = DateField(null=True, blank=True, default=None)
    email = EmailField('email', unique=True, blank=True, null=False)
    phone = CharField(max_length=20, blank=True, default=None, null=True)
    thumbnail = ImageField(blank=True, default='default/default-user.jpg')
    is_verified = BooleanField('verified', default=False)
    verification_uuid = UUIDField('Unique Verification UUID', default=uuid.uuid4)

    @classmethod
    def create(cls, **kwargs):
        new_user = cls()
        new_user.birth_date = kwargs.get('birth_date') if kwargs.get('birth_date') else None
        new_user.email = kwargs.get('email') if kwargs.get('email') else None
        new_user.first_name = kwargs.get('first_name') if kwargs.get('first_name') else None
        new_user.last_name = kwargs.get('last_name') if kwargs.get('last_name') else None
        new_user.password = make_password(kwargs.get('password'))
        new_user.phone = kwargs.get('phone') if kwargs.get('phone') else None
        new_user.username = kwargs.get('username')
        return new_user

    def __str__(self):
        return self.username if self.username else '%s %s' % (self.first_name, self.last_name)


def user_post_save(sender, instance, signal, *args, **kwargs):
    if not instance.is_verified:
        send_verification_email.delay(instance.pk)


signals.post_save.connect(user_post_save, sender=User)

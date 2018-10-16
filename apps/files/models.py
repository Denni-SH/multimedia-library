from django.db.models import (DateTimeField, ImageField, CharField, TextField, FileField, SlugField,
                              ForeignKey, Model, CASCADE)
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify

from multilibrary.settings import AUTH_USER_MODEL

MEDIA_CATEGORIES = ['photo', 'video', 'audio', 'books&docs']


def file_directory_path(instance, filename):
    return f'{instance.owner.pk}/{filename}'


class UserFile(Model):
    title = CharField(blank=True, null=False, max_length=20, default='Default_title', unique=True)
    slug = SlugField(unique=True)
    media_category = CharField(max_length=15, choices=[(item, item) for item in MEDIA_CATEGORIES])
    owner = ForeignKey(AUTH_USER_MODEL, on_delete=CASCADE, related_name='files')
    description = TextField()
    file = FileField(blank=True, null=False, upload_to=file_directory_path)
    thumbnail = ImageField(blank=True, null=False, default='default/default-file.jpg')
    timestamp = DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return '(%s) %s' % (self.pk, self.slug)


@receiver(pre_save, sender=UserFile)
def user_file_pre_save(sender, instance, signal, *args, **kwargs):
    instance.slug = slugify(instance.title)

from rest_framework.serializers import ModelSerializer, CharField

from apps.users.serializers import UserSerializer

from .models import UserFile


class FileSerializer(ModelSerializer):
    file = CharField(max_length=None)
    thumbnail = CharField(max_length=None)
    owner = UserSerializer()

    class Meta:
        model = UserFile
        fields = '__all__'

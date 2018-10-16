from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer, CharField

from apps.users.models import User
from apps.users.serializers import UserSerializer

from .models import UserFile


class FileSerializer(ModelSerializer):
    file = CharField(max_length=None)
    thumbnail = CharField(max_length=None)
    # owner = UserSerializer()
    owner = PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = UserFile
        fields = '__all__'

from django.db.models import Q
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import (SearchFilter,
                                    OrderingFilter,
                                    )

from multilibrary.helpers import generate_formatted_response

from apps.users.permissions import IsVerified

from .models import UserFile
from .serializers import FileSerializer
from .pagination import FilePageNumberPagination
from .filters import FileFilter
from django_filters.rest_framework import DjangoFilterBackend


class FileListView(ListAPIView):
    queryset = UserFile.objects.all()
    serializer_class = FileSerializer
    permission_classes = (IsAuthenticated, IsVerified)
    pagination_class = FilePageNumberPagination
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filter_class = FileFilter
    ordering = ['-timestamp']

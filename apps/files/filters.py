from django_filters import FilterSet, CharFilter, DateTimeFilter
from .models import UserFile


class FileFilter(FilterSet):
    search = CharFilter(field_name='title', lookup_expr='icontains', label="Title")
    m_category = CharFilter(field_name='media_category', label="Type")
    owner_username = CharFilter(field_name='owner__username', label="Owner")
    timestamp = DateTimeFilter(field_name='timestamp', label="Timestamp")

    class Meta:
        model = UserFile
        fields = {
            'owner_id',
            'owner_username',
            'm_category',
            'search',
        }

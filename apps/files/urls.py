from .views import FileListView
from django.urls import path

urlpatterns = [
    path('get_files_list', FileListView.as_view(), name='get_files_list'),
]

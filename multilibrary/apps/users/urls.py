from .views import hello
from django.urls import path

urlpatterns = [
    path('register/', hello)
]

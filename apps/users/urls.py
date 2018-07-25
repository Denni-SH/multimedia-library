from .views import UserCreateView
from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

urlpatterns = [
    path('registration/', UserCreateView.as_view(), name='register'),
    path('login/', obtain_jwt_token, name='login'),
    path('refresh_token/', refresh_jwt_token, name='refresh_token'),
]

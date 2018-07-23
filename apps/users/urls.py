from .views import hello
from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token

urlpatterns = [
    path('register/', hello),
    path('login/', obtain_jwt_token),
    # path('verify_token/', verify_jwt_token),
    path('refresh_token/', refresh_jwt_token),
]

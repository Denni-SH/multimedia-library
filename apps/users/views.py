from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .heplers import valid_mandatory_fields
from .models import User
from .serializers import UserCreateSerializer


class UserCreateView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        try:
            mandatory_fields = {'password', 'first_name', 'username','last_name', 'email'}
            if valid_mandatory_fields(request.data, fields=mandatory_fields):
                user = self.create(request, *args, **kwargs)
                return Response(data={"is_successful": True,
                                      "user": user.data})
            else:
                return Response({"is_successful": False,
                                 "message": 'Mandatory fields are missed!'})
        except Exception as error:
            print(error.__dict__)
            return Response({"is_successful": False,
                                 "message": error.__dict__['detail']['username'][0]})

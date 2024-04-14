# standar libraries
import time

# Django
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

# rest_framework
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import generics, status, permissions

# JWT
from rest_framework_simplejwt.views import TokenObtainPairView

# local Django
from ...models import User
from ..serializers.serializers_login import CustomTokenObtainPairSerializer
from ..serializers.serializers_users import CustomUserSerializer


class Login(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        start_time = time.time()
        try:
            user = authenticate(username=request.data["username"],
                                password=request.data["password"])

            if user and user.is_active:
                login_serializer = self.serializer_class(data=request.data)

                if login_serializer.is_valid():
                    user_serializer = CustomUserSerializer(user)
                    data = {
                        'type':
                        'success',
                        'msg':
                        'Successful Login',
                        'status':
                        status.HTTP_200_OK,
                        'token':
                        login_serializer.validated_data.get('access'),
                        'refresh-token':
                        login_serializer.validated_data.get('refresh'),
                        'user':
                        user_serializer.data,
                    }
                else:
                    raise ValueError(
                        'Contraseña o nombre de usuario incorrectos')
            else:
                raise ValueError(
                    'Incorrect credentials, your account may be inactive')
        except Exception as e:
            data = {
                'type': 'error',
                'msg': str(e),
                'status': status.HTTP_400_BAD_REQUEST
            }
        data['time'] = str(time.time() - start_time)
        return Response(data)


class Logout(GenericAPIView):
    def post(self, request, *args, **kwargs):
        start_time = time.time()
        try:
            user = get_object_or_404(User, id=request.data.get('user'))
            RefreshToken.for_user(user)
            data = {
                'type': 'success',
                'msg': 'Session closed correctly',
                'status': status.HTTP_200_OK,
            }
        except Exception as e:
            data = {
                'type': 'error',
                'msg': str(e),
                'status': status.HTTP_400_BAD_REQUEST
            }
        data['time'] = str(time.time() - start_time)
        return Response(data)

from email.mime.multipart import MIMEMultipart
from django.template.loader import render_to_string
from email.mime.text import MIMEText
import smtplib

from pymysql import DataError
from config import settings

#---------------------------------------------LOGOUT-----------------------------------------------#

from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import generics, status, permissions
#----------------------------------------------EXPIRED---------------------------------------------#

from django.http import HttpResponseRedirect
from datetime import datetime
#---------------------------------------------GENERAL----------------------------------------------#
from ...models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from ..serializers.serializers_login import CustomTokenObtainPairSerializer
from ..serializers.serializers_users import CustomUserSerializer

from django.contrib.auth import authenticate
# from requests import request

class Login(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        data={"status" : status.HTTP_400_BAD_REQUEST }
        try: 
            user = authenticate(
                username=request.data["username"],
                password=request.data["password"]
            )
            if user :
                if user.is_active and user.groups.first():
                    login_serializer = self.serializer_class(data=request.data)
                    if login_serializer.is_valid():
                        user_serializer = CustomUserSerializer(user)
                        data={
                            'token': login_serializer.validated_data.get('access'),
                            'refresh-token': login_serializer.validated_data.get('refresh'),
                            'user': user_serializer.data,
                            'msg': 'Inicio de Sesion Existoso',
                            'status': status.HTTP_200_OK,
                            'type':"success"
                        }
                    else: raise ValueError('Contraseña o nombre de usuario incorrectos')
                else: raise ValueError('Contraseña o nombre de usuario incorrectos')
            else: raise ValueError('Cuenta inactiva o datos incorrectos')
        except Exception as e: 
            data = {'type': 'error', 'msg': str(e)}
        return Response(data, status=data["status"])

class Logout(GenericAPIView):
    def post(self, request, *args, **kwargs):
        user = User.objects.filter(id=request.data.get('user', 0))
        if user.exists():
            RefreshToken.for_user(user.first())
            return Response({'message': 'Sesión cerrada correctamente.'}, status=status.HTTP_200_OK)
        return Response({'error': 'No existe este usuario.'}, status=status.HTTP_400_BAD_REQUEST)
    
            
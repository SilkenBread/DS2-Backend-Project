import uuid

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from apps.user.api.serializers.serializers_users import ActivateAccountSerializer,PasswordSerializer
from apps.user.models import User
from django.contrib.auth.models import Group
from rest_framework.decorators import action
from apps.tools.custom_permissions import CustomPermissions
from django.shortcuts import get_object_or_404
from apps.tools.send_mails import GenericFunctions

class ManageAccount(viewsets.GenericViewSet):
    email = GenericFunctions()
    model = User
    serializers=False
    permission_classes = [permissions.AllowAny]
    def get_object(self, token):
        return get_object_or_404(self.model, token=token)

    """
    Funcion Activate_account -> Activacion de cuenta por medio de token como parametro
    """
    @action(detail=True, methods=['POST'])
    def ActivateAccount(self,request, pk = None):
        data={}
        data["status"] = status.HTTP_400_BAD_REQUEST
        try:
            queryset = self.model.objects.get(token=pk)
            queryset.is_active = True
            queryset.token = uuid.uuid4()
            queryset.save()
            data["status"] = status.HTTP_200_OK; data["msg"] = "Se activo correctamente tu cuenta."; data["type"] =  "success";
        except Exception as e:
            data["type"] = "error"
            data["msg"] = str(e)
        return Response(data, status=data["status"])
    
    """
        Funcion para el cambio de contraseño por correo
        parametros = {
            "password": **STRING**,
            "re_password": **STRING**
        }
    """
    @action(detail=True, methods=['PUT'])
    def ChangePassword(self, request, pk = None):
        data={}
        data["status"] = status.HTTP_400_BAD_REQUEST
        try:
            user = self.get_object(pk)
            serializer = PasswordSerializer(data = request.data)
            if serializer.is_valid():
                user.set_password(serializer.validated_data['password'])
                user.token = uuid.uuid4() 
                user.save()
                data["status"] = status.HTTP_200_OK; data["msg"] = "Se cambio correctamente tu contraseña."
            else:
                data["msg"] = serializer.errors; raise ValueError()
        except Exception as e:
            data["type"] = "error"
            if data.get("msg") is None: data["msg"] = str(e)
        return Response(data, status=data["status"])

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from apps.user.api.serializers.serializers_users import UserSerializer, GroupsSerializer

from apps.user.models import User
from django.contrib.auth.models import Group
from rest_framework.decorators import action
from apps.tools.custom_permissions import CustomPermissions
import uuid
from django.db import transaction

"""
    Funcion "CREATE" del modelo (User), Crea al usuario y le asigna el grupo "Usuario" por defecto.

"""
class userViewSet(viewsets.GenericViewSet):
    permission_classes = [CustomPermissions]
    serializer_class = UserSerializer    
    queryset = None
    model = User

    def get_queryset(self):
        if self.queryset is None:
            self.queryset = self.model.objects.all()
        return self.queryset

    def get_object(self, pk):
        return get_object_or_404(self.model, pk=pk)
    
    #lista Usuarios
    def list(self, request):
        queryset = self.model.objects.filter(is_active=True)
        serializer = self.serializer_class(queryset, many=True) 
        return Response(serializer.data)
    
    #Listar un usuario
    def retrieve(self, request, pk=None): 
        user = self.get_object(pk)
        user_serializer = self.serializer_class(user)
        if not user.is_active:
            return Response({"msg": "Usuario no existe.", "type":"error", "status":400}, status=status.HTTP_400_BAD_REQUEST)
        return Response(user_serializer.data, status=status.HTTP_200_OK)
    
    # Editar Usuarios
    def update(self, request, pk=None):
        user = self.get_object(pk)
        user_serializer = self.serializer_class(user,data = request.data)

        if not user.is_active:
            return Response({"msg": "Usuario no existe.", "type":"error", "status":400}, status=status.HTTP_400_BAD_REQUEST)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({"message":"Usuario actualizado correctamente!"}, status= status.HTTP_200_OK)
        return Response({"error":"hay errores en la actualizacion ", "error": user_serializer.errors}, status= status.HTTP_400_BAD_REQUEST)
    
    # Eliminar Usuarios
    def destroy(self,request,pk = None):
        user_destroy = self.model.objects.filter(id=pk, is_active=True).update(is_active= False)
        if not user_destroy:
            return Response({"msg": "Usuario no existe.", "type":"error", "status":400}, status=status.HTTP_400_BAD_REQUEST)
        if user_destroy == 1:
            return Response({"message":"Usuario eliminado correctamente"},status=status.HTTP_200_OK)
        return Response({"error":"No existe un usuario con estos datos"},status=status.HTTP_404_NOT_FOUND)
    
    def create(self, request):
        data = {'status': status.HTTP_400_BAD_REQUEST}
        """json:
                {
                    "password": "1234",
                    "username": "johan12@gmail.com",
                    "name": "johan",
                    "last_name": "sabogal",
                    "document": 10058375422,
                    "number_phone": 3146446590,
                    "group": 1
                }
        """
        try:
            with transaction.atomic():
                user_serializer = self.serializer_class(data = request.data)

                if user_serializer.is_valid():
                    user_serializer.save(is_active=True)
                    user = User.objects.get(document = request.data["document"])
                    user.save()
                    user.groups.add(Group.objects.get(id=int(request.data["group"])))
                    data["msg"] = "Se ha registrado exitosamente el usuario" ; data["status"] = status.HTTP_201_CREATED; data["type"] = "success";
                else:
                    data["data"] = user_serializer.errors
                    raise ValueError("Ha ocurrido un error en el registro.")
        except Exception as e:
            data.setdefault("msg", str(e))
            data["type"] = "error"
        return Response(data, status = data["status"])
    
    ## Listar Grupos
    @action(detail=False, model=Group, methods=["GET"], url_path="groups")
    def list_groups(self, request):
        return Response(self.model.objects.values('id','name'), status = status.HTTP_200_OK)

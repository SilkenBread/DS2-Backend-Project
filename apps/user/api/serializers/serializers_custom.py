from rest_framework import serializers

class SendMailSerializerCustom(serializers.Serializer):
    email = serializers.EmailField()

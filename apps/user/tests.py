import json

from django.test import TestCase
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from apps.user.api.serializers.serializers_users import UserSerializer


class UserViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.group = Group.objects.create(name="Test Group")
        permissions = Permission.objects.filter(content_type_id=10)
        self.group.permissions.add(*permissions)

        self.user = User.objects.create(username="testuser",
                                        name="Test",
                                        last_name="User",
                                        document=1234567890,
                                        phone_number=1234567890,
                                        is_active=True)
        self.user.groups.add(self.group)
        self.client.force_authenticate(user=self.user)

    def test_list_users(self):
        url = reverse("user-list")
        response = self.client.get(url)
        users = User.objects.filter(is_active=True)
        serializer = UserSerializer(users, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        print('✅ Success test_list_users')

    def test_retrieve_user(self):
        url = reverse("user-detail", args=[self.user.pk])
        response = self.client.get(url)
        serializer = UserSerializer(self.user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        print('✅ Success test_retrieve_user')

    def test_update_user(self):
        url = reverse("user-detail", args=[self.user.pk])
        data = {
            "password": "hoze2024",
            "username": "admin",
            "name": "sebastian",
            "last_name": "orrego",
            "document": "0345363563",
            "number_phone": 3205097741,
            "group": "1"
        }
        response = self.client.put(url,
                                   data=json.dumps(data),
                                   content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, data["name"])
        self.assertEqual(self.user.last_name, data["last_name"])
        print('✅ Success test_update_user')

    def test_delete_user(self):
        url = reverse("user-detail", args=[self.user.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)
        print('✅ Success test_delete_user')

    def test_create_user(self):
        url = reverse("user-list")
        data = {
            "password": "1234",
            "username": "test@example.com",
            "name": "test",
            "last_name": "user",
            "document": 9876543210,
            "phone_number": 9876543210,
            "group": '1'
        }
        response = self.client.post(url,
                                    data=json.dumps(data),
                                    content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(document=data["document"])
        self.assertEqual(user.username, data["username"])
        self.assertEqual(user.name, data["name"])
        self.assertEqual(user.last_name, data["last_name"])
        self.assertEqual(user.phone_number, data["phone_number"])
        print('✅ Success test_create_user')

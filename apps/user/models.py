# stantard library
import uuid

# Django
from django.db import models
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.forms import model_to_dict

from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

# simple_history
from simple_history.models import HistoricalRecords


class UserManager(BaseUserManager):
    def _create_user(self, username, name, last_name, password, is_staff,
                     is_superuser, **extra_fields):
        user = self.model(username=username,
                          name=name,
                          last_name=last_name,
                          is_staff=is_staff,
                          is_superuser=is_superuser,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self,
                    username,
                    name,
                    last_name,
                    password=None,
                    **extra_fields):
        return self._create_user(username, name, last_name, password, False,
                                 False, **extra_fields)

    def create_superuser(self,
                         username,
                         name,
                         last_name,
                         password=None,
                         **extra_fields):
        return self._create_user(username, name, last_name, password, True,
                                 True, **extra_fields)


# Usuario model
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=250, unique=True)
    name = models.CharField('Names', max_length=255, blank=True, null=True)
    token = models.UUIDField('Token',
                             primary_key=False,
                             editable=False,
                             null=True,
                             blank=True)
    last_name = models.CharField('Last names',
                                 max_length=255,
                                 blank=True,
                                 null=True)
    document = models.PositiveBigIntegerField(
        'Document',
        unique=True,
        blank=True,
        null=True,
    )
    phone_number = models.PositiveBigIntegerField('Phone number',
                                                  blank=True,
                                                  null=True)
    is_active = models.BooleanField('State', default=True)
    is_staff = models.BooleanField(default=False)

    historical = HistoricalRecords()
    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def toJSON(self):
        item = model_to_dict(self)
        return item

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'last_name']

    def _str_(self):
        return f'{self.name} {self.last_name}'

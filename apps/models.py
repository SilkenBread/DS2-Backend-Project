from django.db import models
from config.settings import *


class BaseModel(models.Model):
    class Meta:
        abstract = True

    user_creation = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='%(app_label)s_%(class)s_creation',
        null=True,
        blank=True)
    date_creation = models.DateTimeField(auto_now_add=True,
                                         null=True,
                                         blank=True)
    user_updated = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='%(app_label)s_%(class)s_updated',
        null=True,
        blank=True)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

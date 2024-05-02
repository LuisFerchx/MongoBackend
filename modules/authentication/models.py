import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser


class Tenant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'tenant\".\"tenant'


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(max_length=16, blank=True, null=True)
    identification_card = models.CharField(max_length=20, blank=True, null=True)
    token = models.CharField(max_length=500, null=True)
    birthdate = models.CharField(max_length=500, blank=True, null=True)
    tenant = models.ForeignKey(Tenant, related_name='fk_tenant_user', on_delete=models.CASCADE, default=None,
                               blank=True, null=True)
    # sucursal = models.ForeignKey(Sucursal, blank=True, null=True, related_name="fk_sucursal_user",
    #                              on_delete=models.CASCADE)
    # picture = models.FileField(max_length=500, storage=PhotoProfileUserStorage(), blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    REQUIRED_FIELDS = ['email']


class BusinessActivity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    name = models.CharField(max_length=255)
    type = models.SmallIntegerField()
    tenant = models.ForeignKey(Tenant, related_name='fk_tenant_business_activity', on_delete=models.CASCADE,
                               default=None, blank=True, null=True)

    class Meta:
        db_table = 'tenant\".\"business_activity'


class UserDevice(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, related_name="fk_user_userdevice", on_delete=models.CASCADE)
    fb_token = models.CharField(max_length=200, blank=True, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        db_table = 'adm\".\"user_device'
        unique_together = (('user', 'fb_token'),)

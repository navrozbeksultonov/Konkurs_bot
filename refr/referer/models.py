from django.db import models

# Create your models here.
from django.utils.text import slugify


class Log(models.Model):
    user_id = models.BigIntegerField(primary_key=True)
    message = models.JSONField(default={'state': 0})

    def __str__(self):
        return self.user_id


class TgUser(models.Model):
    user_id = models.BigIntegerField(primary_key=True, null=False)
    user_name = models.CharField(max_length=256, null=True)
    first_name = models.CharField(max_length=256, null=True)
    refer_id = models.CharField(max_length=56, null=True)
    odam = models.IntegerField(default=0)
    ball = models.IntegerField(default=0)
    name = models.CharField(max_length=128, null=True)
    phone_number = models.CharField(max_length=15, null=True)
    menu = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.user_id} {self.first_name}"


class referal_friend(models.Model):
    user_id = models.BigIntegerField(primary_key=True, null=False)
    ball = models.IntegerField(default=0)






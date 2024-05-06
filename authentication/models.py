from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _


class AccountManager(BaseUserManager):
    def create_user(self, **kwargs):
        account = self.model(username=kwargs.get("username"))
        account.set_password(kwargs.get("password"))
        account.save()

        return account

    def create_superuser(self, **kwargs):
        account = self.create_user(**kwargs)
        account.is_staff = True
        account.is_superuser = True
        account.is_active = True
        account.save()

        return account


class Account(AbstractUser, PermissionsMixin):

    username = models.CharField(unique=True, max_length=500)
    email = None

    first_name = models.CharField("name", max_length=500)
    last_name = models.CharField(max_length=500, null=True, blank=True)
    last_name = None

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    verify = models.BooleanField(default=True)

    objects = AccountManager()

    USERNAME_FIELD = "username"

    class Meta:
        verbose_name = _("User Management")
        verbose_name_plural = _("User")

    def __str__(self):
        return str(self.first_name)

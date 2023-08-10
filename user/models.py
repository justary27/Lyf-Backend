from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class LyfUserManager(BaseUserManager, models.Manager):

    def create_superuser(self, username, id, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_admin', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_pro_user', True)
        other_fields.setdefault('is_beta_tester', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.',
            )

        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.',
            )

        user = self.create_user(username, id, password, **other_fields)

        print(f"Hello {username} to Lyf!")

        return user

    def create_user(self, username, id, password, **other_fields):

        if not username:
            raise ValueError("")
        else:
            user = self.model(
                id=id,
                username=username,
                **other_fields,
            )

            user.set_password(password)
            user.save()
            
            return user

    def check_if_user_exists(self, user_id):
        return self.filter(id=user_id).exists()

    def get_user_by_id(self, user_id):
        return self.filter(id=user_id).get()

    def get_user_by_username(self, username):
        return self.filter(username=username).get()


# Create your models here.
class LyfUser(AbstractBaseUser, PermissionsMixin):
    """Defining model for the base lyf user."""

    id = models.CharField(
        primary_key=True,
        editable=False,
        auto_created=False,
        max_length=28,
    )

    username = models.CharField(
        _("Username"),
        max_length=80,
        unique=True,
    )

    start_date = models.DateTimeField(
        _("Joined"),
        default=timezone.now,
        editable=False,
        auto_created=True,
    )

    is_pro_user = models.BooleanField(
        _("Lyf Pro"),
        default=False,
    )

    is_beta_tester = models.BooleanField(
        _("Lyf Beta Tester"),
        default=False,
    )

    is_staff = models.BooleanField(
        _("Lyf Staff"),
        default=False,
    )

    is_admin = models.BooleanField(
        _("Lyf Admin"),
        default=False,
    )

    is_active = models.BooleanField(
        _("Active status"),
        default=True,
    )

    USERNAME_FIELD = "username"

    REQUIRED_FIELDS = [
        "id",
    ]

    objects = LyfUserManager()

    def __str__(self) -> str:
        return f"{self.username}"

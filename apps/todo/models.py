import uuid
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from user.models import LyfUser


class TodoManager(models.Manager):

    def get_user_todos(self, user_id) -> list:
        return list(
            self.filter(
                created_by=LyfUser.objects.get_user_by_id(user_id)
            ).all()
        )

    def check_if_todo_exists(self, todo_id):
        return self.filter(id=todo_id).exists()
    
    def get_todo_by_id(self, todo_id):
        return self.filter(id=todo_id).get()


# Create your models here.
class Todo(models.Model):
    """
    Defining model for TODOs in the Todo sub app.
    """

    id = models.UUIDField(
        default=uuid.uuid4,
        auto_created=True,
        primary_key=True,
        editable=False,
        unique=True,
    )

    title = models.CharField(
        _("Title"),
        max_length=120,
        default="Untitled"
    )

    description = models.CharField(
        _("Description"),
        max_length=2048,
    )

    created_by = models.ForeignKey(
        LyfUser,
        on_delete=models.CASCADE,
        editable=False,
    )

    created_on = models.DateTimeField(
        default=timezone.now,
    )

    is_reminder_set = models.BooleanField(
        _("isReminderSet"),
        default=False,
    )

    reminder_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    is_completed = models.BooleanField(
        null=True,
        default=False,
    )

    objects = TodoManager()

    def __str__(self) -> str:
        return f"{self.title} #{self.id}"

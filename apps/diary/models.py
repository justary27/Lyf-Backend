import uuid
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from user.models import LyfUser


class DiaryEntryManager(models.Manager):

    def get_user_entries(self, user_id):
        return list(
            self.filter(
                created_by=LyfUser.objects.get_user_by_id(user_id)
            ).all()
        )

    def get_user_entry(self, user_id, entry_id):
        return self.filter(
            id=entry_id, created_by=LyfUser.objects.get_user_by_id(user_id)
        ).get()

    def check_if_entry_exists(self, entry_id):
        return self.filter(id=entry_id).exists()
    
    def get_entry_by_id(self, entry_id):
        return self.filter(id=entry_id).get()


# Create your models here.
class DiaryEntry(models.Model):
    """
    Defining model for entries in the Diary sub app.
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
        default="Untitled",
    )

    description = models.TextField(
        _("Description"),
    )

    is_private = models.BooleanField(
        default=True,
    )

    created_by = models.ForeignKey(
        LyfUser, 
        on_delete=models.CASCADE,
        editable=False,
    )

    created_on = models.DateTimeField(
        default=timezone.now,
    )

    objects = DiaryEntryManager()

    def __str__(self) -> str:
        return f"{self.title} #{self.id}"

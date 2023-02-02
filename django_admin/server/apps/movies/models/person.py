from django.db import models
from django.utils.translation import gettext_lazy as _

from ..models.common import UUIDMixin, TimeStampedMixin  # noqa: I252


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_("full_name"), max_length=255)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'content"."person'
        indexes = [
            models.Index(fields=["updated_at"], name="person_updated_at_idx"),
        ]
        verbose_name = _("Person")
        verbose_name_plural = _("Persons")

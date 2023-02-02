from django.db import models
from django.utils.translation import gettext_lazy as _

from ..models.common import UUIDMixin, TimeStampedMixin  # noqa: I252


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_("name"), max_length=255)
    description = models.TextField(_("description"), blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'content"."genre'
        indexes = [
            models.Index(fields=["updated_at"], name="genre_updated_at_idx"),
        ]
        verbose_name = _("Genre")
        verbose_name_plural = _("Genres")

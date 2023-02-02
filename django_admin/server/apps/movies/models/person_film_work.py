from django.db import models
from django.utils.translation import gettext_lazy as _
from psqlextra import indexes

from ..models import UUIDMixin  # noqa: I252


class RoleType(models.TextChoices):
    ACTOR = "actor", _("actor")
    WRITER = "writer", _("writer")
    DIRECTOR = "director", _("director")


class PersonFilmwork(UUIDMixin):

    person = models.ForeignKey("Person", on_delete=models.CASCADE, verbose_name=_("Person"), db_index=False)
    film_work = models.ForeignKey("Filmwork", on_delete=models.CASCADE, verbose_name=_("Filmwork"), db_index=False)
    role = models.CharField(_("role"), max_length=10, choices=RoleType.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."person_film_work'
        indexes = [
            indexes.UniqueIndex(fields=["film_work", "person", "role"], name="film_work_person_role_idx"),
        ]
        verbose_name = _("Filmwork person")
        verbose_name_plural = _("Filmwork persons")

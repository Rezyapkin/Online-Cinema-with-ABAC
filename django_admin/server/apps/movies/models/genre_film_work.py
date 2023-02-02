from django.db import models
from django.utils.translation import gettext_lazy as _
from psqlextra import indexes

from ..models import UUIDMixin  # noqa: I252


class GenreFilmwork(UUIDMixin):
    genre = models.ForeignKey("Genre", on_delete=models.CASCADE, verbose_name=_("Genre"), db_index=False)
    film_work = models.ForeignKey("Filmwork", on_delete=models.CASCADE, verbose_name=_("Filmwork"), db_index=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."genre_film_work'
        indexes = [
            indexes.UniqueIndex(fields=["film_work", "genre"], name="film_work_genre_idx"),
        ]
        verbose_name = _("Filmwork genre")
        verbose_name_plural = _("Filmwork genres")

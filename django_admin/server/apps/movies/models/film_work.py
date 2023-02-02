from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from ..models import Genre, Person  # noqa: I252
from ..models.common import UUIDMixin, TimeStampedMixin  # noqa: I252


class FilmworkType(models.TextChoices):
    MOVIE = "movie", _("movie")
    TV_SHOW = "tv_show", _("tv_show")


class FilmworkAgeLimit(models.TextChoices):
    G = "G", _("G")
    PG = "PG", _("PG")
    PG_13 = "PG-13", _("PG-13")
    R = "R", _("R")
    NC_17 = "NC-17", _("NC-17")


class Filmwork(UUIDMixin, TimeStampedMixin):
    title = models.CharField(_("title"), max_length=255)
    description = models.TextField(_("description"), blank=True, null=True)
    creation_date = models.DateField(_("creation_date"), blank=True, null=True)
    rating = models.FloatField(
        _("rating"), validators=[MinValueValidator(0), MaxValueValidator(100)], blank=True, null=True
    )
    type = models.CharField(_("type"), max_length=7, choices=FilmworkType.choices)
    certificate = models.CharField(_("certificate"), max_length=512, blank=True, null=True)
    file_path = models.FileField(_("file"), blank=True, null=True, upload_to="movies/")  # MEDIA_ROOT/movies
    age_limit = models.CharField(_("age_limit"), max_length=7, choices=FilmworkAgeLimit.choices, null=True)

    # allows to add extra data in GenreFilmwork
    genres = models.ManyToManyField(Genre, through="GenreFilmwork")
    persons = models.ManyToManyField(Person, through="PersonFilmwork")

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'content"."film_work'
        indexes = [
            models.Index(fields=["creation_date"], name="film_work_creation_date_idx"),
            models.Index(fields=["updated_at"], name="film_work_updated_at_idx"),
        ]
        verbose_name = _("Filmwork")
        verbose_name_plural = _("Filmworks")

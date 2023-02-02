import uuid

from django.db import models


class TimeStampedMixin(models.Model):
    # auto_now_add автоматически выставит дату создания записи
    created_at = models.DateTimeField(auto_now_add=True)
    # auto_now изменятся при каждом обновлении записи
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True

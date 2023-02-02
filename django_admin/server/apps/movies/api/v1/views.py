from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q, F, Value
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.views.generic import DetailView
from django.views.generic.list import BaseListView

from server.apps.movies.models import Filmwork
from server.apps.movies.models.person_film_work import RoleType


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ["get"]  # Список методов, которые реализует обработчик

    @staticmethod
    def _aggregate_person(role: str):
        return ArrayAgg("persons__full_name", filter=Q(personfilmwork__role=role), distinct=True, default=Value([]))

    @classmethod
    def get_queryset(cls):
        return Filmwork.objects.values(
            "id",
            "title",
            # suppose description and creation_date can be null (based on tests)
            "description",
            "creation_date",
            "type",
        ).annotate(
            rating=Coalesce(F("rating"), Value(0.0)),
            genres=ArrayAgg("genres__name", filter=Q(genres__name__isnull=False), distinct=True, default=Value([])),
            actors=cls._aggregate_person(role=RoleType.ACTOR),
            directors=cls._aggregate_person(role=RoleType.DIRECTOR),
            writers=cls._aggregate_person(role=RoleType.WRITER),
        )

    @staticmethod
    def render_to_response(context):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(queryset, self.paginate_by)
        context = {
            "count": paginator.count,
            "total_pages": paginator.num_pages,
            "prev": page.previous_page_number() if page.has_previous() else None,
            "next": page.next_page_number() if page.has_next() else None,
            "results": list(queryset),
        }
        return context


class MoviesDetailApi(MoviesApiMixin, DetailView):
    def get_context_data(self, **kwargs):
        return kwargs["object"]

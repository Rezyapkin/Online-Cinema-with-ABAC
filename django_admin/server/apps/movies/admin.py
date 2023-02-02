from django.contrib import admin

from .models import Genre, Person, Filmwork, GenreFilmwork, PersonFilmwork


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork
    autocomplete_fields = ("genre",)


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    autocomplete_fields = ("person",)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "created_at", "updated_at")
    search_fields = ("name", "description")


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("full_name", "created_at", "updated_at")
    search_fields = ("full_name",)


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("genres", "persons")

    inlines = (GenreFilmworkInline, PersonFilmworkInline)
    # Отображение полей в списке
    list_display = ("title", "type", "creation_date", "rating", "created_at", "updated_at")
    # Фильтрация в списке
    list_filter = ("type", "creation_date", "rating")
    # Поиск по полям
    search_fields = ("title", "description", "id")

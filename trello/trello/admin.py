from django.contrib import admin

from .models import (
    Card,
    Column,
    Person,
)


@admin.register(Column)
class ColumnsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "order",
    )
    search_fields = ("name",)
    list_filter = ("name",)


@admin.register(Card)
class ColumnsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "author",
        "order",
        "column",
    )
    search_fields = ("name",)
    list_filter = ("author", "column")


@admin.register(Person)
class ColumnsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "nick_name",
    )
    search_fields = ("nick_name",)

from django.conf import settings
from django.contrib import admin

from .models import (
    Card,
    Column,
    User
)


@admin.register(Column)
class ColumnAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "order",
        "dashboard"
    )
    search_fields = (
        "name",
        "dashboard"
    )
    list_filter = ("dashboard",)


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "author",
        "order",
        "column",
    )
    search_fields = ("name",)
    list_filter = (
        "author",
        "column",
    )


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
        "password",
        "is_active",
        "is_staff",
        "is_superuser"
    )
    search_fields = (
        "username",
        "last_name",
        "email",
    )
    empty_value_display = settings.EMPTY_VALUE_DISPLAY

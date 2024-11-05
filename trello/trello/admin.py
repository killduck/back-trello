from django.conf import settings
from django.contrib import admin

from .models import (
    Card,
    Column,
    User,
    CardFile,
    Dashboard,
    DashboardUserRole,
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
        "order",
        "column",
    )
    search_fields = ("name",)
    list_filter = (
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
        "img",
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


@admin.register(CardFile)
class CardFileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "card",
        "name",
        "size",
        "extension",
        "date_upload",
        "file_url",
        "image"
    )
    search_fields = ("name",)


@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "img"
    )
    search_fields = ("name",)
    list_filter = (
        "name",
    )


@admin.register(DashboardUserRole)
class DashboardUserRoleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "dashboard",
        "user",
        "role"

    )
    list_filter = (
        "dashboard",
    )

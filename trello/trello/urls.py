from django.contrib import admin
from django.urls import path

from . import views


urlpatterns = [
    path("columns/", views.columns, name="columns"),
    path("dashboards/", views.dashboards, name="dashboards"),
    path("swap-columns/", views.swap_columns, name="swap-columns"),
    path("create-column/", views.create_column, name="create-column"),
    path("delete-column/", views.delete_column, name="delete-column"),
    # path("columns/edite/", views.columns_edite, name="columns-edite"),
    path("cards/", views.cards, name="cards"),
    # path('test/', views.test, name='test'),
    path("admin/", admin.site.urls),
]

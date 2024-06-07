from django.contrib import admin
from django.urls import path

from . import views


urlpatterns = [
    path("columns/", views.columns, name="columns"),
    path("swap-columns/", views.swap_columns, name="swap-columns"),
    path("create-columns/", views.create_columns, name="create-columns"),
    path("delete-columns/", views.delete_columns, name="delete-columns"),
    # path("columns/edite/", views.columns_edite, name="columns-edite"),
    path("cards/", views.cards, name="cards"),
    # path('test/', views.test, name='test'),
    path("admin/", admin.site.urls),
]

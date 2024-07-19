from django.contrib import admin
from django.urls import path

from . import views


urlpatterns = [
    path('login/', views.CustomAuthToken.as_view(), name="token-create"),
    path('logout/', views.token_destroy, name="token-destroy"),
    path("dashboards/", views.dashboards, name="dashboards"),
    path("dashboard-role/", views.dashboard_role, name="dashboard-role"),
    path("columns/", views.columns, name="columns"),
    path("take-data-column/", views.take_data_column, name="take-data-column"),
    path("new-data-column/", views.new_data_column, name="new_data_column"),
    path("take-data-card/", views.take_data_card, name="take-data-card"),
    path("new-data-card/", views.new_data_card, name="new_data_card"),
    path("swap-columns/", views.swap_columns, name="swap-columns"),
    path("swap-cards/", views.swap_cards, name="swap-cards"),
    path("create-column/", views.create_column, name="create-column"),
    path("create-card/", views.create_card, name="create-card"),
    path("delete-column/", views.delete_column, name="delete-column"),
    path("delete-card/", views.delete_card, name="delete-card"),
    path("admin/", admin.site.urls),
]

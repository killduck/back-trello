from django.contrib import admin
from django.urls import path

from . import views


urlpatterns = [
    path('login/', views.CustomAuthToken.as_view(), name="token-create"),
    path('logout/', views.token_destroy, name="token-destroy"),
    path("dashboards/", views.dashboards, name="dashboards"),
    path("columns/", views.columns, name="columns"),
    path("column/", views.column, name="column"),
    # path("cards/", views.cards, name="cards"),
    path("card/", views.card, name="card"),
    path("swap-columns/", views.swap_columns, name="swap-columns"),
    path("swap-cards/", views.swap_cards, name="swap-cards"),
    path("create-column/", views.create_column, name="create-column"),
    path("create-card/", views.create_card, name="create-card"),
    path("delete-column/", views.delete_column, name="delete-column"),
    path("test-api/", views.test_api, name="test-api"),
    # path("columns/edite/", views.columns_edite, name="columns-edite"),
    # path('test/', views.test, name='test'),
    path("admin/", admin.site.urls),
]

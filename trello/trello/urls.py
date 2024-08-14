from django.contrib import admin
from django.urls import include, path

from . import views


urlpatterns = [
    path(
        'api/',  # сюда позже добавить приставку api/
        include(
            [
                path('login/', views.CustomAuthToken.as_view(), name="token-create"),
                path('logout/', views.token_destroy, name="token-destroy"),
                path('user/', views.user, name="user"),
                path("dashboards/", views.dashboards, name="dashboards"),
                path("dashboard-role/", views.dashboard_role, name="dashboard-role"),
                # path("card-user/", views.card_user, name="card-user"),
                path("dashboard-user/", views.dashboard_user, name="dashboard-user"),
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
                path("card-user-update/", views.card_user_update, name="card-user-update"),
                path("card-user-delete/", views.card_user_delete, name="card-user-delete"),
                path("send-mail/", views.send_mail, name="send-mail"),
                path("label-data/", views.label_data, name="label-data"),
                path("add-label-to-card/", views.add_label_to_card, name="add-label-to-card"),
                path("add-card-description/", views.add_card_description, name="add-card-description"),
                path("search-role-board/", views.search_role_board, name="search-role-board"),
                path("change-role-board/", views.change_role_board, name="change-role-board"),
                path("test/", views.test),
                path("test2/", views.test2),
            ]
        ),
    ),
    path("admin/", admin.site.urls),
]

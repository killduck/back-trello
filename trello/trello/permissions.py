from rest_framework.permissions import SAFE_METHODS, BasePermission

from .models import (
    DashboardUserRole,
    User
)


class IsUserHasRole(BasePermission):
    """
    Ограничиваем пользовательские разрешения, что бы
    пользовтаель не першел по URLу на дашборд, где он не имеет ролей.
    """

    def has_permission(self, request, view):
        user = request.user

        if request.method == "POST":
            dashboard_id = request.data["dashboardId"]
            users_in_dashboard = DashboardUserRole.objects.values('user').filter(dashboard=dashboard_id)
            obj_users = User.objects.filter(id__in=users_in_dashboard)

            return (
                user and user.is_authenticated
            ) and user in obj_users

        return (user and user.is_authenticated)

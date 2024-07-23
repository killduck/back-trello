from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import (
    api_view,
    permission_classes,
)

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import (
    Card,
    Column,
    Dashboard,
    DashboardUserRole,
    User,
    CardUser
)
from .permissions import (
   IsUserHasRole,
)
from .serializers import (
    CardSerializer,
    ColumnSerializer,
    DashboardSerializer,
    DashboardUserRoleSerializer,
    UserSerializer,
    CardUserSerializer,
)


# Кастомное представление, что бы была возможность возвращать в Response не только Token
class CustomAuthToken(ObtainAuthToken):
    """Кастомный вьюсета для получения Token."""

    def post(self, request, *args, **kwargs):

        username = request.data.get('username', None)
        password = request.data.get('password', None)

        if username is None or password is None:
            return Response(
                {'error': 'Нужен и логин, и пароль'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                'token': token.key,
                'user_id': user.pk,
                'user_name': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'user_email': user.email,
                'success': 'Можно еще, что-нибудь вернуть - кроме денег!!! :)'
            },
            status=status.HTTP_200_OK
        )


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def user(request):

    auth_user = request.user.id

    queryset = get_object_or_404(User, id=auth_user)
    serializer = UserSerializer(queryset, many=False)

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def token_destroy(request):
    print(request.headers['Authorization'])
    token = request.headers['Authorization'][6:]
    Token.objects.get(key=token).delete()
    return Response(
        {
            'success': 'Токен удален'
        },
        status=status.HTTP_200_OK
    )


@api_view(["GET", "POST"])
# @permission_classes([AllowAny])
@permission_classes([IsAuthenticated])
def columns(request):

    dashboard_id = request.data["dashboardId"]

    queryset = Column.objects.all().filter(dashboard=dashboard_id)
    serializer = ColumnSerializer(queryset, many=True)

    return Response(serializer.data)


@api_view(["GET", "POST"])
@permission_classes([IsUserHasRole])  # кастомный пермишен, что бы пользователь не смог через URL получить доступ к доске, где у него нет прав/ролей
def dashboards(request):

    auth_user = request.user.id

    if request.method == "POST":
        dashboard_id = request.data["dashboardId"]
        queryset = get_object_or_404(Dashboard, id=dashboard_id)
        serializer = DashboardSerializer(queryset, many=False)
        return Response(serializer.data)

    queryset = Dashboard.objects.filter(dashboard_user_role__user_id=auth_user)
    serializer = DashboardSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["POST"])
# @permission_classes([AllowAny])
@permission_classes([IsAuthenticated])
def swap_columns(request):

    dashboard_id = request.data["dashboardId"]

    try:
        for column in request.data["columns"]:
            Column.objects.filter(id=column["id"]).update(order=column["order"])
        print("обновили порядок колонок в БД")
    except:
        print("если что-то сюда прилетит, то будем разбираться")
        return Response(False, status=status.HTTP_404_NOT_FOUND)

    queryset = Column.objects.filter(dashboard=dashboard_id)
    serializer = ColumnSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["POST"])
# @permission_classes([AllowAny])
@permission_classes([IsAuthenticated])
def swap_cards(request):

    try:
        for card in request.data["order_cards"]:
            Card.objects.filter(id=card["id"]).update(
                order=card["order"], column=card["column"]
            )
        print("обновили порядок карточек в БД")
    except:
        print("если что-то сюда прилетит, то будем разбираться")
        return Response(False, status=status.HTTP_404_NOT_FOUND)

    dashboard_id = request.data["dashboardId"]

    list_column = Column.objects.filter(dashboard=dashboard_id)

    queryset = Card.objects.filter(column_id__in=list_column)
    serializer = CardSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def create_column(request):
    # TODO добавить параметры idWorkSpace: 1 ?? уже не суждено

    dashboard_columns = request.data["idDashboard"]

    last_column_order = Column.objects.filter(dashboard=dashboard_columns).last()

    if last_column_order:
        order = last_column_order.order + 1
    else:
        order = 0

    try:
        new_add_column = Column.objects.create(
            name=request.data["nameNewColumn"],
            order=order,
            dashboard_id=request.data["idDashboard"],
        )
    except:
        return Response(False, status=status.HTTP_404_NOT_FOUND)

    serializer = ColumnSerializer(new_add_column)
    return Response(serializer.data)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def create_card(request):

    card_column = request.data["column"]
    last_card_in_column = Card.objects.filter(column=card_column).last()

    if last_card_in_column:
        order = last_card_in_column.order + 1
    else:
        order = 0

    try:
        new_add_card = Card.objects.create(
            name=request.data["name"],
            order=order,
            column_id=request.data["column"],
        )

    except:
        return Response(False, status=status.HTTP_404_NOT_FOUND)

    serializer = CardSerializer(new_add_card)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def delete_column(request):
    try:
        id_column_deleted = request.data["id_column"]
        if id_column_deleted:
            Column.objects.filter(id=id_column_deleted).delete()
    except:
        return Response(False, status=status.HTTP_404_NOT_FOUND)
    return Response(True, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def delete_card(request):
    try:
        id_card_deleted = request.data["id_card"]
        if id_card_deleted:
            Card.objects.filter(id=id_card_deleted).delete()
    except:
        return Response(False, status=status.HTTP_404_NOT_FOUND)
    return Response(True, status=status.HTTP_200_OK)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def take_data_column(request):
    if request.data['id']:
        column_id = request.data['id']
        queryset = Column.objects.all().filter(id=column_id)

    serializer = ColumnSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def take_data_card(request):
    if request.data['id']:
        card_id = request.data['id']
        queryset = Card.objects.all().filter(id=card_id)

    serializer = CardSerializer(queryset, many=True)
    print(serializer.data)
    return Response(serializer.data)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def new_data_card(request):
    if request.data['id'] and request.data['name']:
        card_id = request.data['id']
        card_new_name = request.data['name']
        try:
            Card.objects.filter(id=card_id).update(name=card_new_name)
        except:
            print("если что-то сюда прилетит, то будем разбираться")
            return Response(False, status=status.HTTP_404_NOT_FOUND)

        queryset = Card.objects.all().filter(id=card_id)
        serializer = CardSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def new_data_column(request):
    if request.data['id'] and request.data['name']:
        column_id = request.data['id']
        column_new_name = request.data['name']
        try:
            Column.objects.filter(id=column_id).update(name=column_new_name)
        except:
            print("если что-то сюда прилетит, то будем разбираться")
            return Response(False, status=status.HTTP_404_NOT_FOUND)

        queryset = Column.objects.all().filter(id=column_id)
        serializer = ColumnSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["GET", "POST"])
# @permission_classes([AllowAny])
# @permission_classes([IsAuthenticated])
@permission_classes([IsUserHasRole])
def dashboard_role(request):
    queryset = DashboardUserRole.objects.all()
    serializer = DashboardUserRoleSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def card_user_update(request):
    # print(request.data)
    if request.data['user_id'] and request.data['card_id']:
        user_id = request.data['user_id']
        card_id = request.data['card_id']

        try:
            new_card_user, created = CardUser.objects.get_or_create(
                card_id=card_id,
                user_id=user_id,
            )
        except:
            print("если что-то сюда прилетит, то будем разбираться")
            return Response(False, status=status.HTTP_404_NOT_FOUND)

        card_user_serializer = CardUserSerializer(new_card_user).data
        queryset = User.objects.all().filter(id=card_user_serializer['user_id'])
        user_serializer = UserSerializer(queryset, many=True).data[0]

        return Response(
            {
                "id": card_user_serializer['id'],
                "card_id": card_user_serializer['card_id'],
                "user_id": card_user_serializer['user_id'],
                "user_data": user_serializer,
            },
            status=status.HTTP_200_OK,
        )


@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def card_user_delete(request):
    if request.data['user_id'] and request.data['card_id']:
        user_id = request.data['user_id']
        try:
            if CardUser.objects.filter(user_id=user_id):
                CardUser.objects.filter(user_id=user_id).delete()
            else:
                return Response(False, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(False, status=status.HTTP_404_NOT_FOUND)

        return Response(True, status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def dashboard_user(request):

    dashboard_id = request.data["dashboardId"]

    users = DashboardUserRole.objects.values('user').filter(dashboard=dashboard_id)
    queryset = User.objects.filter(id__in=users)
    serializer = UserSerializer(queryset, many=True)
    return Response(serializer.data)

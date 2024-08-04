from django.conf import settings
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
    CardUser,
    Label,
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
    LabelSerializer,
)
from .utils import SendMessage


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
def label_data(request):

    queryset = Label.objects.all()
    serializer = LabelSerializer(queryset, many=True)

    return Response(serializer.data)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def add_label_to_card(request):
    if request.data['card_id'] and request.data['label_id'] or (request.data['label_id'] is None):
        card_id = request.data['card_id']
        label_id = request.data['label_id']
        try:
            Card.objects.filter(id=card_id).update(label_id=label_id)
        except:
            print("если что-то сюда прилетит, то будем разбираться")
            return Response(False, status=status.HTTP_404_NOT_FOUND)

        queryset = Card.objects.all().filter(id=card_id)
        serializer = CardSerializer(queryset, many=True)
        return Response(serializer.data)
    else:
        return Response(False, status=status.HTTP_404_NOT_FOUND)


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
    print(request.data)
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
    auth_user = request.user.id
    print(request.data)
    if request.data['id']:
        column_id = request.data['id']
        queryset = Column.objects.all().filter(id=column_id)

        serializer_column = ColumnSerializer(queryset, many=True).data
        return Response(
            {
                "column": serializer_column,
                "auth_user": auth_user,
            },
            status=status.HTTP_200_OK,
        )
    else:
        return Response(False, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def take_data_card(request):
    auth_user = request.user.id
    if request.data['id']:
        card_id = request.data['id']
        queryset_card = Card.objects.all().filter(id=card_id)

        card_users = CardUser.objects.values('user').filter(card_id=card_id)
        card_users_data = User.objects.filter(id__in=card_users)

        serializer_card_users_data = UserSerializer(card_users_data, many=True).data
        serializer_card = CardSerializer(queryset_card, many=True).data

        return Response(
            {
                "card": serializer_card,
                "card_users_data": serializer_card_users_data,
                "auth_user": auth_user,
            },
            status=status.HTTP_200_OK,
        )
    else:
        return Response(False, status=status.HTTP_404_NOT_FOUND)


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
    else:
        return Response(False, status=status.HTTP_404_NOT_FOUND)


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
    else:
        return Response(False, status=status.HTTP_404_NOT_FOUND)


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

        queryset = User.objects.all().filter(id=new_card_user.user_id)
        user_serializer = UserSerializer(queryset, many=True).data[0]

        return Response(user_serializer)
    else:
        return Response(False, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def card_user_delete(request):
    if request.data['user_id'] and request.data['card_id']:
        user_id = request.data['user_id']
        card_id = request.data['card_id']
        try:
            CardUser.objects.filter(card_id=card_id, user_id=user_id).delete()
        except:
            return Response(False, status=status.HTTP_404_NOT_FOUND)

        return Response(True, status=status.HTTP_200_OK)
    else:
        return Response(False, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def dashboard_user(request):
    dashboard_id = request.data["dashboardId"]

    users = DashboardUserRole.objects.values('user').filter(dashboard=dashboard_id)
    queryset = User.objects.filter(id__in=users)
    serializer = UserSerializer(queryset, many=True)

    return Response(serializer.data)


@api_view(["POST"])
# @permission_classes([AllowAny])
@permission_classes([IsAuthenticated])
def send_mail(request):

    request = request.data

    """
    образец_принимаемого_объекта = {
    *** Основные поля которые нужно направлять на роут send-mail/ ***
        "addres_mail" : "Raa78@mail.ru",  # поле с адресом получателя
        "subject_letter" : "The subject of the letter",  #  поле с темой письма не обязательное, но желательно
        "text_letter" : "Текст сообщения",  # поле с текстом сообщения (ради этого и  делаем)
        "method" : "smtp",  # выбор способа отправки почты smtp/console/file - по умолчанию пишет в консоль
    *** Не обязательные поля, буду формироваться из значений по умолчанию ***
        "type_message" : "add_dashboard",  # вид шаблона сообщения, если не указан берется пустая строка + text_letter
        "fail_silently" : True,  # указывает сообщать (True) об ошибках или нет(False)
        "sender_email": "python31@top-python31.ru"  # почтовый сервер, по умолчанию забит адрес почты хоста
    *** Поле для хеширования сообщения, еще в работе, думаю пока над функционалом ***
        "hash text" : {
            "algorithm" : "sha256"
        }
    }
    """

    if request and request.get('addres_mail') != None:

        message = request['text_letter']

        check_type_letter = request.get('type_message'),

        letter = {
            'subject_letter' : request.get('subject_letter', ''),
            'text_letter' : settings.MAIL_MESSAGE[check_type_letter[0]] + message if check_type_letter[0] != None else settings.MAIL_MESSAGE['empty'] + message,
            'addres_mail' : [request['addres_mail']],
        }

        send = SendMessage(
            letter,
            request.get('method'),
            request.get('fail_silently', False),
            request.get('sender_email')
            )
        send.get_send_email

        return Response(True)

    return Response(False)

from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string

from datetime import datetime

from django.conf import settings
from django.shortcuts import get_object_or_404, get_list_or_404

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
    Role,
    Label, Activity,
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
    LabelSerializer, ActivitySerializer,
)
from .utils import SendMessage, PreparingMessage

from .views_functions.sending_email import sending_email


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
def add_card_description(request):
    # print(request.data)
    if request.data['card_id'] and request.data['description'] or (request.data['description'] is None):
        card_id = request.data['card_id']
        description = request.data['description']
        try:
            Card.objects.filter(id=card_id).update(description=description)
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
def add_card_activity(request):
    print(f'129__ {request.data}')
    card_users = CardUserSerializer(CardUser.objects.values('user_id').filter(card_id=request.data['card_id']).
                                    exclude(user_id=request.data['author_id']), many=True).data
    # print(f'132__ {card_users}')
    if request.data['card_id'] and request.data['author_id'] and request.data['comment']:
        action_text = 'обновил'
        ''' Это нужно при создании нового коммента '''
        if request.data['find_by_date'] == 'no':
            action_text = 'добавил'
            request.data['find_by_date'] = datetime.now()

        Activity.objects.update_or_create(
            date=request.data['find_by_date'],
            defaults={
                'comment': request.data['comment'],
                'action': f'{action_text}(а) комментарий',
            },
            create_defaults={
                'card_id': request.data['card_id'],
                'author_id': request.data['author_id'],
                'comment': request.data['comment'],
                'action': f'{action_text}(а) комментарий',
            }
        )

        queryset_activity = Activity.objects.filter(card_id=request.data['card_id']).reverse()
        serializer_activity = ActivitySerializer(queryset_activity, many=True).data
        # print(f'156__ {serializer_activity[0]['author']}')

        ''' тут отправим письмо каждому юзеру карточки '''
        mail_data = ActivitySerializer(Activity.objects.filter(date=request.data['find_by_date']).
                                       filter(), many=True).data
        print(f'161__ {mail_data[0]}')
        for card_user in card_users:
            print(f'163__ {card_user['user_id']}')
            card_users_data = UserSerializer(User.objects.filter(id=card_user['user_id']), many=True).data[0]
            print(f'165__ {card_users_data["email"]}, {request.data['card_id']}')

            message = PreparingMessage(
                subject_letter=f'Изменение в карточке {request.data['card_id']}',
                text_letter=f'{mail_data[0]["author"]["first_name"]} '
                            f'{mail_data[0]["author"]["last_name"]} '
                            f'{action_text}(а) комментарий, созданный: '
                            f'{mail_data[0]["date"]}',
                template='',
            )
            send = SendMessage(
                letter=message.get_message,
                addres_mail=[card_users_data["email"]]
            )
            send.get_send_email
            send.get_output_to_console

        return Response(serializer_activity)
    else:
        return Response(False, status=status.HTTP_404_NOT_FOUND)



@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def del_card_activity(request):
    # print(request.data)
    try:
        id_comment = request.data["comment_id"]
        Activity.objects.filter(id=id_comment).delete()
    except:
        return Response(False, status=status.HTTP_404_NOT_FOUND)
    return Response(True, status=status.HTTP_200_OK)


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
@permission_classes([IsAuthenticated])
def swap_cards(request):
    print(request.data)
    try:
        column_name_start = Card.objects.filter(id=request.data['card_id'])[0].column

        for card in request.data["order_cards"]:
            Card.objects.filter(id=card["id"]).update(
                order=card["order"], column=card["column"]
            )

        column_name_end = Card.objects.filter(id=request.data["card_id"])[0].column

        if request.user.id and request.data['card_id'] and (column_name_start != column_name_end):
            action_text = f'переместил(а) эту карточку из колонки "{column_name_start}" в колонку "{column_name_end}"'
            Activity.objects.create(
                card_id=request.data['card_id'],
                author_id=request.user.id,
                comment=None,
                action=action_text,
            )
            ''' тут отправим письмо каждому юзеру карточки '''
            card_users = CardUserSerializer(
                CardUser.objects.values('user_id').filter(card_id=request.data['card_id']).
                exclude(user_id=request.user.id), many=True
            ).data
            mail_data = ActivitySerializer(Activity.objects.last(), many=False).data
            card_data = CardSerializer(Card.objects.filter(id=request.data['card_id']), many=True).data[0]
            # print(card_users, mail_data, card_data['name'])
            for card_user in card_users:
                card_users_data = UserSerializer(User.objects.filter(id=card_user['user_id']), many=True).data[0]
                subject_email = f'Изменение в карточке {card_data['name']}'
                text_email = (f'{mail_data["author"]["first_name"]} '
                              f'{mail_data["author"]["last_name"]} '
                              f'{action_text}.')
                address_mail = card_users_data['email']
                # print(f'304__ {card_users_data["email"]}, {request.data['card_id']}')
                # print(f'302__ {card_user["user_id"]}, {mail_data["card"]}')
                print(f'test__333\n')
                sending_email(subject_email, text_email, address_mail)
                print(f'test__333\n')

            print("обновили порядок карточек в БД")
    except Exception as err:
        print(f'если что-то сюда прилетит, то будем разбираться: \n {err}')
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
    # print(request.data)
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
    # print(request.data)
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
@permission_classes([IsUserHasRole])
def dashboard_role(request):
    queryset = DashboardUserRole.objects.all()
    serializer = DashboardUserRoleSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def card_user_update(request):
    print(request.data)
    if request.data['user_id'] and request.data['card_id']:
        user_id = request.data['user_id']
        card_id = request.data['card_id']
        card_data = CardSerializer(Card.objects.filter(id=request.data['card_id']), many=True).data[0]

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

        if request.data['auth_user']:
            action_text = f"добавил(а) участника \"{user_serializer['username']}\" к карточке \"{card_data['name']}\""
            if user_id == request.data['auth_user']:
                action_text = f"присоединился(-лась) к карточке \"{card_data['name']}\""

            ''' тут пишем добавленных пользователей на карточку в БД '''
            Activity.objects.create(
                card_id=request.data['card_id'],
                author_id=request.data['auth_user'],
                comment=None,
                action=action_text,
            )

            ''' тут отправим письмо каждому юзеру карточки '''
            card_users = CardUserSerializer(
                CardUser.objects.values('user_id').filter(card_id=request.data['card_id']).
                exclude(user_id=request.user.id), many=True
            ).data
            mail_data = ActivitySerializer(Activity.objects.last(), many=False).data
            card_data = CardSerializer(Card.objects.filter(id=request.data['card_id']), many=True).data[0]
            # print(f'545__{card_users}\n, _______{mail_data}\n, _______{card_data}\n')

            for card_user in card_users:
                card_users_data = UserSerializer(User.objects.filter(id=card_user['user_id']), many=True).data[0]
                subject_email = f'Изменение в карточке {card_data['name']}'
                text_email = (f'{mail_data["author"]["first_name"]} '
                              f'{mail_data["author"]["last_name"]} '
                              f'{action_text}.')
                address_mail = card_users_data['email']

                sending_email(subject_email, text_email, address_mail)

        return Response(user_serializer)
    else:
        return Response(False, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def card_user_delete(request):
    """
        Cорри, я немного подчистил представление, т.к. сказать соблюдем DRY и уберем лишние пустые условия
        Так же воспользуемся методом get() и зададим условие:
         - если в словаре не находится ключ, то get() вернет False
         - если ключ есть, вернется значение ключа
        Ну и воспользуемся функцией get_object_or_404(). Если по зачениям ключей выборка объекта будет уходит в ошибку,
        get_object_or_404() выкинет автоматом 404
    """
    # TODO Если нет возражений, комментарий-пояснение можно удалить
    print(request.data)
    user_id = request.data.get('user_id', False)
    card_id = request.data.get('card_id', False)

    dashboard_id = request.data.get('dashboard_id', False)

    card_users = CardUserSerializer(
        CardUser.objects.values('user_id').filter(card_id=request.data['card_id']).
        exclude(user_id=request.user.id), many=True
    ).data

    if user_id and card_id:
        card_user = get_object_or_404(CardUser, card_id=card_id, user_id=user_id)
        card_user.delete()

        if request.data['auth_user']:
            queryset = User.objects.all().filter(id=user_id)
            user_serializer = UserSerializer(queryset, many=True).data[0]
            card_data = CardSerializer(Card.objects.filter(id=request.data['card_id']), many=True).data[0]

            action_text = f"убрал(а) участника \"{user_serializer['username']}\" из карточке \"{card_data['name']}\""
            if user_id == request.data['auth_user']:
                action_text = f"покинул(а) карточку \"{card_data['name']}\""

            ''' тут пишем удалённых пользователей с карточки в БД '''
            Activity.objects.create(
                card_id=request.data['card_id'],
                author_id=request.data['auth_user'],
                comment=None,
                action=action_text,
            )

            ''' тут отправим письмо каждому юзеру карточки '''
            mail_data = ActivitySerializer(Activity.objects.last(), many=False).data

            for card_user in card_users:
                card_users_data = UserSerializer(User.objects.filter(id=card_user['user_id']), many=True).data[0]
                subject_email = f'Изменение в карточке {card_data['name']}'
                text_email = (f'{mail_data["author"]["first_name"]} '
                              f'{mail_data["author"]["last_name"]} '
                              f'{action_text}.')
                address_mail = card_users_data['email']

                sending_email(subject_email, text_email, address_mail)

        return Response(True, status=status.HTTP_200_OK)

    if user_id and dashboard_id:
        card = get_list_or_404(Card, column__dashboard_id = dashboard_id)
        card_user = CardUser.objects.filter(card_id__in = card, user_id=user_id)
        card_user.delete()
        return Response(True, status=status.HTTP_200_OK)

    return Response(False, status=status.HTTP_404_NOT_FOUND)
    # TODO Если нет возражений, закомментированный код можно удалить
    #     try:
    #         CardUser.objects.filter(card_id=card_id, user_id=user_id).delete()
    #     except:
    #         return Response(False, status=status.HTTP_404_NOT_FOUND)

    #     return Response(True, status=status.HTTP_200_OK)
    # else:
    #     return Response(False, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def dashboard_user(request):
    dashboard_id = request.data["dashboardId"]

    if request.data["dashboardId"].isdigit():

        users = DashboardUserRole.objects.values('user').filter(dashboard=dashboard_id)
        queryset = User.objects.filter(id__in=users)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    return Response(False, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def send_mail(request):

    """
    образец_принимаемого_объекта = {
    *** Основные поля которые нужно направлять на роут send-mail/ ***
        "subject_letter" - поле с темой письма не обязательное, но желательно
        "text_letter" - поле с текстом сообщения (ради этого и  делаем)
        "template": "add_dashboard" или "deadline" # вид шаблона текста письма.
                                                    Берется из settings.py из переменной MAIL_MESSAGE.
                                                    Поле можно опустить.
        "addres_mail" : "Raa78@mail.ru",  # поле с адресом получателя (обязательно)
    }

    ОБРАЗЕЦ
    {
        "subject_letter": "Обрарить внимание",
        "text_letter": "Qwerty & asdfgh",
        "template": "deadline",
        "addres_mail": "Raa78@mail.ru"
    }
    """

    request = request.data

    if request:

        message = PreparingMessage(
            subject_letter = request.get('subject_letter', ''),
            text_letter = request.get('text_letter', ''),
            template = request.get('template', '')
        )

        send = SendMessage(
            letter = message.get_message,
            addres_mail = [request['addres_mail']]
        )

        send.get_send_email
        # отправляем email. Либо:
        # - send.get_write_to_file = записать в файл send.get_write_to_file
        # - send.get_output_to_console = вывести в консоль send.get_output_to_console
        return Response(True)

    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def search_role_board(request):
    # print('search_role_board>>>', request.data)

    user_auth_id = request.user.id
    user_card_id = request.data['user_id']
    active_boards = request.data['dashboard_id']

    users_on_board = DashboardUserRole.objects.filter(dashboard_id = active_boards)

    try:

        role_auth_user = users_on_board.filter(user_id=user_auth_id).values('role__name').first()['role__name']

        role_card_user = users_on_board.filter(user_id=user_card_id).values('role__name').first()['role__name']

        count_user_on_board = users_on_board.count()

        count_admin_on_board = users_on_board.filter(role__name = 'admin').count()


        role_parameters = {
            'user_auth_id': user_auth_id,
            'role_auth_user': role_auth_user,
            'user_card_id': user_card_id,
            'role_card_user': role_card_user,
            'count_user_on_board': count_user_on_board,
            'count_admin_on_board': count_admin_on_board,
        }

        return Response(role_parameters)
    except:
        return Response(False)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def change_role_board(request):

    user_id = request.data['user_id']

    active_boards = request.data['dashboard_id']

    users_on_board = DashboardUserRole.objects.filter(dashboard_id = active_boards,
                                                      user_id = user_id)

    changeable_user_role = users_on_board.first().role.name


    user_auth_id = request.user.id

    user_auth_on_board = DashboardUserRole.objects.filter(dashboard_id = active_boards,
                                                      user_id = user_auth_id).first()

    user_auth_role = user_auth_on_board.role.name

    count_admins_on_board = DashboardUserRole.objects.filter(dashboard_id = active_boards,
                                                      role__name = 'admin').count()

    print('changeable_user_role>>>', changeable_user_role)

    if (request.data['action'] == 'add_admin' and
        user_auth_role == 'admin'):

        role_admin = get_object_or_404(Role, name='admin').id
        users_on_board.update(role_id=role_admin)
        return Response(True,status=status.HTTP_200_OK)

    if (request.data['action'] == 'del_admin' and
        user_auth_role == 'admin' and
        count_admins_on_board > 1):

        role_participant = get_object_or_404(Role, name='participant').id
        users_on_board.update(role_id=role_participant)
        return Response(True,status=status.HTTP_200_OK)

    if request.data['action'] == 'del_user':
        if changeable_user_role == 'admin' and not user_auth_role == "admin":
            print('?????')
            pass

        users_on_board.delete()
        return Response(True,status=status.HTTP_200_OK)

    return Response(False, status=status.HTTP_404_NOT_FOUND)


# @api_view(["POST"])
# @permission_classes([AllowAny])
# def test_view(request):

#     {
#         "subject_letter":"Моя тема",
#         "text_letter": "Qwerty&ksdghkgsghlak",
#         "template":"add_dashboard",
#         "addres_mail": "rubtsov1978@gmail.com"
#     }


#     {
#         "subject_letter":"Моя тема",
#         "text_letter": "Тестовое сообщение для проверки функционала.",
#         "addres_mail": "rubtsov1978@gmail.com"
#     }

#     request = request.data

#     if request:
#         message = PreparingMessage(
#             subject_letter = request.get('subject_letter', ''),
#             text_letter = request.get('text_letter', ''),
#             template = request.get('template', '')
#         )

#         send = SendMessage(
#             letter = message.get_message,
#             addres_mail = [request['addres_mail']]
#         )

#         send.get_send_email
#         send.get_write_to_file
#         send.get_output_to_console

#         return Response(True)

#     return Response(status=status.HTTP_404_NOT_FOUND)

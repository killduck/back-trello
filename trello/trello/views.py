from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, get_list_or_404
from django.db.models import Q

from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import (
    action,
    api_view,
    permission_classes,
)

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .Classes.AddFileAndLink import AddFileAndLink
from .models import (
    Activity,
    Card,
    CardFile,
    CardImg,
    CardLink,
    CardUser,
    Column,
    Dashboard,
    DashboardUserRole,
    InvitUserDashboard,
    ImageExtension,
    Label,
    Role,
    User,
)

from .permissions import (IsUserHasRole)
from .serializers import (
    ActivitySerializer,
    CardSerializer,
    CardUserSerializer,
    CardImgSerializer,
    CardFileSerializer,
    ColumnSerializer,
    DashboardSerializer,
    DashboardUserRoleSerializer,
    InvitUserDashboardSerializer,
    ImageExtensionSerializer,
    LabelSerializer,
    UserSearchSerializer,
    UserSerializer,
)
from .utils import (
    Hash,
    PreparingMessage,
    SendMessage,
)
from .views_functions.add_file_link import add_file, add_link
from .views_functions.sending_email import sending_email
from .views_functions.take_favicon import take_favicon


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def add_file_and_link_to_card(request):
    add_error = AddFileAndLink(request)
    card_data = CardSerializer(Card.objects.filter(id=request.data['card_id']), many=True).data[0]
    if add_error.error_file and add_error.error_link:
        return Response(False, status=status.HTTP_404_NOT_FOUND)
    return Response(card_data, status=status.HTTP_200_OK)

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def download_file_from_card(request):
    try:
        file_id = int(request.data['file_id'])
        uploaded_file = CardFile.objects.get(id=file_id)
        response = HttpResponse(uploaded_file.file_url, content_type='application/force-download')
        response['Content-Disposition'] = f'attachment; filename="{uploaded_file.name}"'
        return response
    except Exception as ex:
        print(f'error => {ex}')
        return Response(False, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def del_file_from_card(request):
    try:
        card_id = request.data["card_id"]
        file_id = request.data["file_id"]
        if card_id and file_id:
            CardFile.objects.filter(id=file_id).delete()

            card_data = CardSerializer(Card.objects.filter(id=card_id), many=True).data[0]
            return Response(card_data, status=status.HTTP_200_OK)
    except:
        return Response(False, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def del_link_from_card(request):
    try:
        card_id = request.data["card_id"]
        link_id = request.data["link_id"]
        if card_id and link_id:
            CardLink.objects.filter(id=link_id).delete()

            card_data = CardSerializer(Card.objects.filter(id=card_id), many=True).data[0]
            return Response(card_data, status=status.HTTP_200_OK)
    except:
        return Response(False, status=status.HTTP_404_NOT_FOUND)


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
    if request.data['card_id'] and request.data['label_id'] and request.data['label_text']:
        card_id = request.data['card_id']
        if request.data['label_id'] == 'null':
            label_id = None
            label_text = None
        else:
            label_id = request.data['label_id']

            if request.data['label_text'] == 'null':
                label_text = None
            else:
                label_text = request.data['label_text']

        try:
            Card.objects.filter(id=card_id).update(label_id=label_id, label_text=label_text)
        except Exception as ex:
            print(f"если что-то сюда прилетит, то будем разбираться, {ex}")
            return Response(False, status=status.HTTP_404_NOT_FOUND)

        queryset = Card.objects.all().filter(id=card_id)
        serializer = CardSerializer(queryset, many=True)
        return Response(serializer.data)
    else:
        return Response(False, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def add_card_description(request):
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
    if request.data['card_id'] and request.data['author_id'] and request.data['comment']:
        card_users = CardUserSerializer(
            CardUser.objects.values('user_id').filter(card_id=request.data['card_id']).
            exclude(user_id=request.data['author_id']), many=True).data
        action_text = 'обновил'
        date_time_now = request.data['find_by_date']

        ''' Это нужно при создании нового коммента '''
        if request.data['find_by_date'] == 'no':
            action_text = 'добавил'
            date_time_now = datetime.now().strftime("%Y-%m-%d %H:%M:00")
        ''' пишем в базу '''
        Activity.objects.update_or_create(
            date=date_time_now,
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

        ''' тут отправим письмо каждому юзеру карточки '''
        if request.data['find_by_date'] == 'no':
            mail_data = ActivitySerializer(Activity.objects.last(), many=False).data
        else:
            mail_data = ActivitySerializer(
                Activity.objects.filter(date=request.data['find_by_date']), many=True).data[0]

        card_data = CardSerializer(Card.objects.filter(id=request.data['card_id']), many=True).data[0]
        comment_date = datetime.strptime(mail_data["date"], "%Y-%m-%dT%H:%M:%S.%f")
        comment_date_nice_format = comment_date.strftime("%Y.%m.%d %H:%M:%S")

        if mail_data["comment"] is not None:
            comment_text = f'Текст комментария: \n\"{mail_data["comment"][3: -4]}\"'
        else:
            comment_text = f'Текст комментария: нет"'

        for card_user in card_users:
            card_users_data = UserSerializer(User.objects.filter(id=card_user['user_id']), many=True).data[0]

            subject_email = f'Изменение в карточке \"{card_data["name"]}\"'
            text_email = (f'{mail_data["author"]["first_name"]} '
                          f'{mail_data["author"]["last_name"]} '
                          f'{action_text}(а) комментарий, '
                          f'созданный {comment_date_nice_format} '
                          f'в карточке \"{card_data["name"]}\".\n'
                          f'Текст комментария: \n\"{comment_text}\"')
            address_mail = card_users_data['email']
            sending_email(subject_email, text_email, address_mail)

        ''' для отправки на фронт в развёрнутом порядке '''
        queryset_activity = Activity.objects.filter(card_id=request.data['card_id'])
        serializer_activity = ActivitySerializer(queryset_activity, many=True).data

        return Response(serializer_activity)
    else:
        return Response(False, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def del_card_activity(request):
    try:
        id_comment = request.data["comment_id"]
        Activity.objects.filter(id=id_comment).delete()
    except:
        return Response(False, status=status.HTTP_404_NOT_FOUND)

    return Response(True, status=status.HTTP_200_OK)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def add_card_due_date(request):
    if request.data['card_id'] and request.data['end_date_time']:
        card_id = request.data['card_id']
        end_date_time = datetime.strptime(request.data['end_date_time'], "%d-%m-%Y %H:%M:%S")
        try:
            Card.objects.filter(id=card_id).update(date_end=end_date_time)
        except Exception as ex:
            print("если что-то сюда прилетит, то будем разбираться", ex)
            return Response(False, status=status.HTTP_404_NOT_FOUND)

        queryset = Card.objects.all().filter(id=card_id)
        serializer = CardSerializer(queryset, many=True)
        return Response(serializer.data)
    else:
        return Response(False, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def del_card_due_date(request):
    if request.data['card_id']:
        card_id = request.data['card_id']
        try:
            Card.objects.filter(id=card_id).update(date_end=None, execute= False)
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
def add_card_due_date_execute(request):
    try:
        card_id = request.data['card_id']
        card_execute = request.data['card_execute']
        if card_execute == 'true':
            card_execute = True
        elif card_execute == 'false':
            card_execute = False
        Card.objects.filter(id=card_id).update(execute=card_execute)
    except Exception as ex:
        print("если что-то сюда прилетит, то будем разбираться", ex)
        return Response(False, status=status.HTTP_404_NOT_FOUND)

    queryset = Card.objects.filter(id=card_id)
    serializer = CardSerializer(queryset, many=True)
    return Response(serializer.data)


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
    try:
        column_name_start = Card.objects.filter(id=request.data['card_id'])[0].column
        for card in request.data["order_cards"]:
            Card.objects.filter(id=card["id"]).update(
                order=card["order"], column=card["column"]
            )
        column_name_end = Card.objects.filter(id=request.data["card_id"])[0].column

        if request.user.id and request.data['card_id'] and (column_name_start != column_name_end):
            action_text = f'переместил(а) эту карточку из колонки "{column_name_start}" в колонку "{column_name_end}"'
            ''' пишем в базу action'''
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

            for card_user in card_users:
                card_users_data = UserSerializer(User.objects.filter(id=card_user['user_id']), many=True).data[0]
                subject_email = f'Изменение в карточке {card_data['name']}'
                text_email = (f'{mail_data["author"]["first_name"]} '
                              f'{mail_data["author"]["last_name"]} '
                              f'{action_text}.')
                address_mail = card_users_data['email']
                sending_email(subject_email, text_email, address_mail)
            print("обновили порядок карточек в БД")
    except Exception as ex:
        print(f'если что-то сюда прилетит, то будем разбираться: \n {ex}')
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
    auth_user = request.user.id
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
            return Response(False, status=status.HTTP_404_NOT_FOUND)
        users_on_board.delete()
        return Response(True,status=status.HTTP_200_OK)

    return Response(False, status=status.HTTP_404_NOT_FOUND)

class InvitUserBoardViewSet(viewsets.ModelViewSet):

    # queryset = InvitUserDashboard.objects.all()
    # serializer_class = InvitUserDashboardSerializer

    @action(
            detail=False,
            methods=['post',],
            permission_classes=(IsAuthenticated,),
            url_path='select-users',
    )
    def select_users(self, request):
        data_to_search = request.data['fieldData'].strip().lower()

        dashboard = request.data['dashboardId']

        # Пользователи, которые есть на доске
        users_on_board = DashboardUserRole.objects.filter(dashboard_id = dashboard).values('user__username')

        # Пользователи, которые приглашены на доску
        already_invited_users = InvitUserDashboard.objects.filter(dashboard_id = dashboard).values('user__username')

        search_result = []

        if len(data_to_search) < 1:
            return Response(search_result, status=status.HTTP_200_OK)

        search_result = User.objects.filter(
            Q(username__icontains=data_to_search) |
            Q(email__icontains=data_to_search)
        ).exclude(username__in=users_on_board).exclude(username__in=already_invited_users).values('username', 'email')

        serializer = UserSearchSerializer(search_result, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
            detail=False,
            methods=['post',],
            permission_classes=(IsAuthenticated,),
            url_path='invit-users',
    )
    def invit_users(self, request):
        request = request.data

        list_of_invited_users = request['selectedOption']

        if not list_of_invited_users:
            return Response('No user', status=status.HTTP_204_NO_CONTENT)


        # получаем имя доски для добавления в строку для хэширования
        dashboard_name = Dashboard.objects.filter(id=request['dashboardId']).values_list('name', flat=True).first()

        # print('invit_users>>>', list_of_invited_users, dashboard_name)
        for user in list_of_invited_users:
            user_id = User.objects.filter(username = user['username']).values_list('id', flat=True).first()

            hash = Hash(dashboard_name + user['email'])
            hash_message = hash.get_hash_sha256

            InvitUserDashboard.objects.create(
            dashboard_id=int(request['dashboardId']),
            user_id=user_id,
            hash=hash_message,
            )

            message = PreparingMessage(
                subject_letter = 'Приглашение на доску',
                text_letter = hash_message,
                template = 'add_dashboard'
            )

            send = SendMessage(
            letter = message.get_message,
            addres_mail = [user['email']]
            )

            send.get_send_email

        return Response(True, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['post',],
        permission_classes=(IsAuthenticated,),
        url_path='list-invited-users',
    )
    def list_invited_users(self, request):

        dashboard_id = request.data['dashboardId']

        already_invited_users = User.objects.filter(user_dashboard_invate__dashboard=dashboard_id)  # выборку делаем через related_name

        serializer = UserSerializer(already_invited_users, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['post',],
        permission_classes=(IsAuthenticated,),
        url_path='pending-confirmations',
    )
    def pending_confirmation(self, request):
        invit_hash = request.data['alias']
        find_invite = InvitUserDashboard.objects.filter(hash=invit_hash).first()
        role_participant = get_object_or_404(Role, name='participant')

        if find_invite:
            DashboardUserRole.objects.create(
            dashboard=find_invite.dashboard,
            user=find_invite.user,
            role=role_participant
            )
            find_invite.delete()
            response_data = {
                'status': True,
                'board_name': find_invite.dashboard.name,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        return Response({'status': False})


class СheckRegistrationUserViewSet(viewsets.ModelViewSet):


    @action(
            detail=False,
            methods=['post',],
            permission_classes=(AllowAny,),
            url_path='check-username',
    )

    def check_username(self, request):
        data_to_search = request.data['fieldNickNameData'].strip()

        search_result = User.objects.filter(username=data_to_search)


        response_data = {
                'status': None,
                'nick_name': None,
                'message': None,
        }


        if search_result:

            response_data['status'] = False
            response_data['nick_name'] = data_to_search,
            response_data['message'] = 'Такой ник уже есть',

            return Response(response_data, status=status.HTTP_200_OK)

        response_data['status'] = True

        response_data['nick_name'] = data_to_search,

        response_data['message'] = 'Ник свободен',

        return Response(response_data, status=status.HTTP_200_OK)

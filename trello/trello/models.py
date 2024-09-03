from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


# Cправочные материалы по API для компонентов системы аутентификации Django https://docs.djangoproject.com/en/5.0/ref/contrib/auth/
class User(AbstractUser):
    """Переопределяем стандартную модель User."""

    username = models.CharField(
        db_index=True,
        max_length=150,
        unique=True,
        error_messages={
            'unique': 'Пользователь с таким логином уже существует.',
        },
        validators=[
            RegexValidator(
                regex=r'^[-a-zA-Z0-9_]+$',
                message='Не допустимое имя'
            )
        ],
        verbose_name='Логин',
        help_text='Введите логин пользователя',
    )
    email = models.EmailField(
        max_length=200,
        unique=True,
        error_messages={
            'unique': 'Пользователь с таким e-mail уже существует.',
        },
        verbose_name='Email',
        help_text='Введите email пользователя',
    )
    first_name = models.CharField(
        max_length=200,
        verbose_name='Имя',
        help_text='Введите имя пользователя',
    )
    last_name = models.CharField(
        max_length=200,
        verbose_name='Фамилия',
        help_text='Введите фамилию пользователя',
    )
    img = models.ImageField(
        max_length=200,
        null=True,
        verbose_name="Фото пользователя",
    )
    #  Помечает учетную запись пользователя как активную. Django рекомендуеn установить этот флаг равным False вместо удаления учетных записей.
    is_active = models.BooleanField(
        default=True,
        verbose_name="Запись активна",
    )
    # Позволяет этому пользователю получить доступ к сайту администратора.
    is_staff = models.BooleanField(
        default=False,
        verbose_name="права Админа",
    )
    # Рассматривает пользователя как имеющего все разрешения, не назначая ему никаких разрешений в частности.
    is_superuser = models.BooleanField(
        default=False,
        verbose_name="права СуперПользователя",
    )

    USERNAME_FIELD = 'email'  # уазываем, что входим по email, а не по username
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
        'password'
    ]

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Dashboard(models.Model):
    """Модель для досок."""

    name = models.CharField(
        max_length=50,
        verbose_name="Наименование доски",
        help_text="Введите наименование доски",
    )
    img = models.ImageField(
        max_length=200,
        null=True,
        verbose_name="Картинка доски(фон)",
    )

    class Meta:
        verbose_name = "Дашборд"
        verbose_name_plural = "дашборды"

    def __str__(self):
        return self.name


class Column(models.Model):
    """Модель для колонок."""

    name = models.CharField(
        max_length=50,
        verbose_name="Наименование колонки",
        help_text="Введите наименование колонки",
    )
    order = models.IntegerField(
        verbose_name="Номер позиции колонки",
        help_text="Номер позиции",
        null=True,
    )
    dashboard = models.ForeignKey(
        "Dashboard",
        on_delete=models.CASCADE,
        related_name="column",
        verbose_name="Дашборд",
        help_text="Введите Дашборд к которому относится колонка",
        # null=True,
    )

    class Meta:
        verbose_name = "Колонку"
        verbose_name_plural = "колонки"
        ordering = [
            "order",
        ]

    def __str__(self):
        return self.name


class Label(models.Model):
    """Модель для цветовых меток."""

    name = models.CharField(
        max_length=50,
        verbose_name="Наименование цветовой метки",
        help_text="Введите наименование цветовой метки",
    )
    color_hex = models.CharField(
        max_length=200,
        verbose_name="Hex цвета",
        help_text="Введите hex код цвета",
    )

    class Meta:
        verbose_name = "Метка"
        verbose_name_plural = "метки"
        ordering = ["id"]

    def __str__(self):
        return self.name


class Activity(models.Model):
    """Модель для действий в карточке."""
    # поправить не нужные null=True
    author = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name="activity",
        blank=True,
        null=True,
        verbose_name="Пользователь",
        help_text="Введите пользователя к которой описывает действие",
    )
    card = models.ForeignKey(
        "Card",
        on_delete=models.CASCADE,
        related_name="activity",
        blank=True,
        null=True,
        verbose_name="Карточка",
        help_text="Введите карточку к которой относится действие",
    )
    date = models.DateTimeField(
        auto_now=False,
        auto_now_add=True,
        blank=True,
        null=True,
    )
    comment = models.TextField(
        max_length=500,
        verbose_name="Комментарий к карточке",
        help_text="Введите комментарий к карточке",
        null=True,
    )
    action = models.TextField(
        max_length=200,
        verbose_name="Изменение в карточке",
        help_text="Введите изменение в карточке",
        null=True,
    )

    class Meta:
        verbose_name = "Действия"
        verbose_name_plural = "действие"
        ordering = ["id"]

    def __str__(self):
        return self.text


class Card(models.Model):
    """Модель для карточек задач."""

    name = models.CharField(
        max_length=50,
        verbose_name="Наименование карточки",
        help_text="Введите наименование карточки",
    )
    order = models.IntegerField(
        verbose_name="Номер позиции карточки",
        help_text="Введите номер позиции карточки",
    )
    column = models.ForeignKey(
        "Column",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="cards",
        verbose_name="Колонка",
        help_text="Введите колонку к которой относится карточка",
    )
    date_start = models.DateField(
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True,
    )
    date_end = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True,
    )
    label = models.ForeignKey(
        "Label",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="cards",
        verbose_name="Метка",
        help_text="Введите цветовую метку",
    )
    description = models.TextField(
        verbose_name="Текст описания карточки",
        help_text="Введите текст",
        max_length=500,
        null=True,
    )

    class Meta:
        verbose_name = "Карточку"
        verbose_name_plural = "карточки"
        ordering = [
            "order",
        ]

    def __str__(self):
        return self.name


class Role(models.Model):
    """Модель для списка ролей."""

    name = models.CharField(
        max_length=50,
        verbose_name="Наименование роли",
        help_text="Введите наименование роли",
    )
    description = models.CharField(
        max_length=200,
        verbose_name="Описание роли",
        help_text="Введите описание роли",
    )

    class Meta:
        verbose_name = "Роль"
        verbose_name_plural = "роли"
        ordering = [
            "name",
        ]

    def __str__(self):
        return self.name


class DashboardUserRole(models.Model):
    """Модель для ролей юзеров в дашборде."""

    dashboard = models.ForeignKey(
        "Dashboard",
        on_delete=models.CASCADE,
        related_name="dashboard_user_role",
        verbose_name="Дашборд",
    )
    user = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name="user_dashboard",
        verbose_name="Пользователь",
    )
    role = models.ForeignKey(
        "Role",
        on_delete=models.CASCADE,
        related_name="role_dashboard",
        verbose_name="Роль",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['dashboard', 'user'],
                name='unique_dashboard_user'
            )
        ]

    def __str__(self):
        return (
            f'В дашборде={self.dashboard.name} пользователь={self.user.username} '
            f'имеет роль={self.role.name}.'
        )


class CardUser(models.Model):
    """Модель для ролей юзеров в карточке."""

    card = models.ForeignKey(
        "Card",
        on_delete=models.CASCADE,
        related_name="card_user_role",
        verbose_name="Карточка",
    )
    user = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name="user_card",
        verbose_name="Польователь",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['card', 'user'],
                name='unique_card_user'
            )
        ]

    def __str__(self):
        return (
            f'В карточке={self.card.name} пользователь={self.user.username} '
            # f'имеет роль={self.role.name}.'
        )


class Checklist(models.Model):
    """Модель для чек-листа."""

    name = models.CharField(
        max_length=50,
        verbose_name="Наименование чек-листа",
        help_text="Введите наименование чек-листа",
    )
    card = models.ForeignKey(
        "Card",
        on_delete=models.CASCADE,
        related_name="checklist",
        verbose_name="Карточка",
    )

    class Meta:
        verbose_name = "Чеклист"
        verbose_name_plural = "чеклисты"

    def __str__(self):
        return self.name


class Checkstep(models.Model):
    """Модель задачек для чек-листа."""

    text = models.TextField(
        verbose_name="Текст чекбокса",
        help_text="Введите текст",
    )
    checkbox = models.BooleanField()
    checklist = models.ForeignKey(
        "Checklist",
        on_delete=models.CASCADE,
        related_name="checkstep",
        verbose_name="Чек-лист",
    )

    class Meta:
        verbose_name = "Чекбокс"
        verbose_name_plural = "чекбоксы"

    def __str__(self):
        return self.text


# class InvitUserDashboard(models.Model):
#     """Модель для приглашения юзеров на доску."""

#     dashboard = models.ForeignKey(
#         "Dashboard",
#         on_delete=models.CASCADE,
#         related_name="dashboard_user_invait",
#         verbose_name="Дашборд",
#     )
#     user = models.ForeignKey(
#         "User",
#         on_delete=models.CASCADE,
#         related_name="user_dashboard_invate",
#         verbose_name="Пользователь",
#     )
#     hash = models.TextField(
#         verbose_name="Значение хэша",
#         help_text="Введите значение хэша",
#     )

#     class Meta:
#         constraints = [
#             models.UniqueConstraint(
#                 fields=['dashboard', 'user'],
#                 name='unique_dashboard_user'
#             )
#         ]

#     def __str__(self):
#         return (
#             f'На дашборд={self.dashboard.name} приглашен пользователь={self.user.username}.'
#         )

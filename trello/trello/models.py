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


# class WorkSpace(models.Model):
#     """Модель для рабочих пространств."""

#     name = models.CharField(
#         max_length=50,
#         verbose_name="Наименование колонки",
#         help_text="Введите наименование колонки",
#     )
#     order = models.IntegerField(
#         verbose_name="Номер позиции колонки",
#         help_text="Номер позиции",
#         # unique=True,
#         # error_messages={
#         #     "unique": "Номер позиции повторяется",
#         # },
#         null=True,
#     )

#     class Meta:
#         verbose_name = "Колонку"
#         verbose_name_plural = "колонки"
#         ordering = [
#             "order",
#         ]

#     def __str__(self):
#         return self.name


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


class Card(models.Model):
    """Модель для карточек задач."""

    name = models.CharField(
        max_length=50,
        verbose_name="Наименование карточки",
        help_text="Введите наименование карточки",
    )
    author = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name="cards",
        verbose_name="Автор",
        help_text="Введите автора",
        # null=True,
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

    class Meta:
        verbose_name = "Карточку"
        verbose_name_plural = "карточки"
        ordering = [
            "order",
        ]

    def __str__(self):
        return self.name


# class Person(models.Model):
#     """Модель для пользователей."""

#     first_name = models.CharField(
#         max_length=50,
#         blank=True,
#         null=True,
#         verbose_name="Имя",
#         help_text="Введите Имя",
#     )
#     last_name = models.CharField(
#         max_length=50,
#         blank=True,
#         null=True,
#         verbose_name="Фамилия",
#         help_text="Введите Фамилию",
#     )
#     nick_name = models.CharField(
#         max_length=50,
#         unique=True,
#         error_messages={
#             "unique": "Такой Никнейм уже есть",
#         },
#         verbose_name="Никнейм",
#         help_text="Введите Никнейм",
#     )

#     class Meta:
#         verbose_name = "Участник"
#         verbose_name_plural = "участники"
#         ordering = [
#             "nick_name",
#         ]

#     def __str__(self):
#         return self.nick_name

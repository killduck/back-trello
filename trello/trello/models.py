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
        verbose_name="Польователь",
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
                fields=['dashboard', 'user', 'role'],
                name='unique_dashboard_role'
            )
        ]

    def __str__(self):
        return (
            f'В дашборде={self.dashboard.name} пользователь={self.user.username} '
            f'имеет роль={self.role.name}.'
        )


class CardUserRole(models.Model):
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
    role = models.ForeignKey(
        "Role",
        on_delete=models.CASCADE,
        related_name="role_card",
        verbose_name="Роль",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['card', 'user', 'role'],
                name='unique_card_role'
            )
        ]

    def __str__(self):
        return (
            f'В карточке={self.card.name} пользователь={self.user.username} '
            f'имеет роль={self.role.name}.'
        )

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

from .models_functions.upload_files_img import (
    upload_to_files,
    upload_to_images,
)

class ImageExtension(models.Model):
    type= models.CharField(
        max_length=50,
        verbose_name="Расширение фото",
        help_text="Введите расширение фото",
        blank=True,
        null=True,
    )

class CardLink(models.Model):
    text = models.CharField(
        max_length=500,
        verbose_name="Имя ссылки",
        help_text="Введите ссылку",
        blank=True,
        null=True,
    )
    description = models.CharField(
        max_length=500,
        verbose_name="описание ссылки",
        help_text="Введите описание ссылки",
        blank=True,
        null=True,
    )
    favicon = models.CharField(
        max_length=200,
        verbose_name="Имя ссылки для фавикона",
        help_text="Введите ссылку для фавикона",
        blank=True,
        null=True,
    )
    first_letter = models.CharField(
        max_length=10,
        verbose_name="первая буква ссылки",
        help_text="Введите первую букву ссылки",
        blank=True,
        null=True,
    )
    card = models.ForeignKey(
        "Card",
        on_delete=models.CASCADE,
        related_name="card_link",
        blank=True,
        null=False,
        verbose_name="Карточка",
        help_text="Введите карточку к которой относится ссылка",
    )

class CardImg(models.Model):
    card = models.ForeignKey(
        "Card",
        on_delete=models.CASCADE,
        related_name="card_img",
        blank=True,
        null=False,
        verbose_name="Карточка",
        help_text="Введите карточку к которой относится фото",
    )
    name = models.CharField(
        max_length=50,
        verbose_name="Имя фото",
        help_text="Введите имя фото",
        blank=True,
        null=True,
    )
    size = models.IntegerField(
        verbose_name="Размер фото",
        help_text="Введите размер фото",
        null=True,
    )
    extension = models.CharField(
        max_length=50,
        verbose_name="расширение фото",
        help_text="Введите расширение фото",
        blank=True,
        null=True,
    )
    date_upload = models.DateTimeField(
        auto_now=True,
        auto_now_add=False,
        blank=True,
        null=True,
    )
    image_url = models.ImageField(
        upload_to=upload_to_images,
        blank=True,
        null=True,
    )
    image = models.BooleanField(
        default=True,
        verbose_name="фото или нет",
    )


class CardFile(models.Model):
    card = models.ForeignKey(
        "Card",
        on_delete=models.CASCADE,
        related_name="card_file",
        blank=True,
        null=False,
        verbose_name="Карточка",
        help_text="Введите карточку к которой относится файл",
    )
    name = models.CharField(
        max_length=50,
        verbose_name="Имя файла",
        help_text="Введите имя файла",
        blank=True,
        null=True,
    )
    size = models.IntegerField(
        verbose_name="Размер файла",
        help_text="Введите размер к файла",
        null=True,
    )
    extension = models.CharField(
        max_length=50,
        verbose_name="расширение файла",
        help_text="Введите расширение файла",
        blank=True,
        null=True,
    )
    date_upload = models.DateTimeField(
        auto_now=True,
        auto_now_add=False,
        blank=True,
        null=True,
    )
    file_url = models.FileField(
        upload_to=upload_to_files,
        blank=True,
        null=True,
    )
    image = models.BooleanField(
        default=False,
        verbose_name="фото или нет",
    )

# Справочные материалы по API для компонентов системы аутентификации Django https://docs.djangoproject.com/en/5.0/ref/contrib/auth/
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
    execute = models.BooleanField(
        default=False,
        verbose_name="выполнить до срока",
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

# тут удаляем файл
@receiver(pre_delete, sender=CardFile)
def image_model_delete(sender, instance, **kwargs):
    if instance.file_url.name:
        instance.file_url.delete(False)
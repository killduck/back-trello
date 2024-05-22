from django.db import models


class Column(models.Model):
    """Модель для колонок."""

    name = models.CharField(
        max_length=50,
        verbose_name="Наименование колонки",
        help_text="Введите наименование колонки",
    )
    order = models.IntegerField(
        verbose_name="Номер позиции колонки",
        help_text="Введите номер позиции",
        unique=True,
        error_messages={
            "unique": "Номер позиции повторяется",
        },
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
        "Person",
        on_delete=models.CASCADE,
        related_name="cards",
        verbose_name="Автор",
        help_text="Введите автора",
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


class Person(models.Model):
    """Модель для польователей."""

    first_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Имя",
        help_text="Введите Имя",
    )
    last_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Фамилия",
        help_text="Введите Фамилию",
    )
    nick_name = models.CharField(
        max_length=50,
        unique=True,
        error_messages={
            "unique": "Такой Никнейм уже есть",
        },
        verbose_name="Никнейм",
        help_text="Введите Никнейм",
    )

    class Meta:
        verbose_name = "Участник"
        verbose_name_plural = "участники"
        ordering = [
            "nick_name",
        ]

    def __str__(self):
        return self.nick_name

from trello.models import (
    Column, Card,
    Dashboard, DashboardUserRole,
    Role, User, Label,
)

tables = [
    {
        "table_name": Label,
        "table_dada": [
            {
                "id": 1,
                "name": "green",
                "color_hex": "#216e4e",
            },
            {
                "id": 2,
                "name": "yellow",
                "color_hex": "#ffff00",
            },
            {
                "id": 3,
                "name": "orange",
                "color_hex": "#ffa500",
            },
            {
                "id": 4,
                "name": "red",
                "color_hex": "#ae2e24",
            },
            {
                "id": 5,
                "name": "purple",
                "color_hex": "#800080",
            },
            {
                "id": 6,
                "name": "blue",
                "color_hex": "#0055cc",
            },
        ],
    },
    {
        "table_name": Dashboard,
        "table_dada": [
            {
                "id": 1,
                "name": "Diplom 31",
                "img": "background_desert.webp"
            },
            {
                "id": 2,
                "name": "Тестовая доска",
                "img": "Background_blue.svg"
            },
        ],
    },
    {
        "table_name": Column,
        "table_dada": [
            {
                "id": 1,
                "name": "backlog",
                "order": 0,
                "dashboard": Dashboard(id=1)
            },
            {
                "id": 2,
                "name": "Test column #1",
                "order": 0,
                "dashboard": Dashboard(id=2),
            },
            {
                "id": 3,
                "name": "Test column #2",
                "order": 1,
                "dashboard": Dashboard(id=2),
            },
            {
                "id": 4,
                "name": "in progress",
                "order": 1,
                "dashboard": Dashboard(id=1),
            },
            {
                "id": 5,
                "name": "done",
                "order": 2,
                "dashboard": Dashboard(id=1),
            },
        ],
    },
    {
        "table_name": User,
        "table_dada": [
            {
                "id": 2,
                "username": "Raa78",
                "first_name": "Андрей",
                "last_name": "Рубцов",
                "email": "Raa78@mail.ru",
                "is_active": True,
                "is_staff": False,
                "is_superuser": False,
                "password": "Raa78",
            },
            {
                "id": 3,
                "username": "ilya616",
                "first_name": "Илья",
                "last_name": "Полетуев",
                "email": "ilya616@mail.ru",
                "is_active": True,
                "is_staff": False,
                "is_superuser": False,
                "password": "ilya616",
            },
            {
                "id": 4,
                "username": "killduck",
                "first_name": "Леонид",
                "last_name": "Кильдюшев",
                "email": "killduck@mail.ru",
                "is_active": True,
                "is_staff": False,
                "is_superuser": False,
                "password": "killduck",
            },
            {
                "id": 5,
                "username": "admin",
                "first_name": "Админ",
                "last_name": "Админов",
                "email": "admin@mail.ru",
                "is_active": True,
                "is_staff": True,
                "is_superuser": True,
                "password": 'admin',
            },
            {
                "id": 6,
                "username": "vasya",
                "first_name": "Вася",
                "last_name": "Пупкин",
                "email": "vasya@mail.ru",
                "is_active": True,
                "is_staff": False,
                "is_superuser": False,
                "password": 'vasya',
            },
        ],
    },
    {
        "table_name": Card,
        "table_dada": [
            {
                "id": 1,
                "name": "ES Lint",
                "order": 0,
                "column": Column(id=1),
                "label": Label(id=1),
            },
            {
                "id": 2,
                "name": "Лёня хреначит реакт компоненты",
                "order": 1,
                "column": Column(id=1),
                "label": Label(id=2),
            },
            {
                "id": 3,
                "name": "Task #1",
                "order": 0,
                "column": Column(id=2),
                "label": Label(id=3),
            },
            {
                "id": 4,
                "name": "Task #2",
                "order": 1,
                "column": Column(id=2),
                "label": Label(id=4),
            },
            {
                "id": 5,
                "name": "Кнопки меню",
                "order": 0,
                "column": Column(id=4),
                "label": Label(id=5),
            },
            {
                "id": 6,
                "name": "Search button",
                "order": 1,
                "column": Column(id=4),
                "label": Label(id=6),
            },
            {
                "id": 7,
                "name": "Task #3",
                "order": 0,
                "column": Column(id=3),
                "label": Label(id=1),
            },
            {
                "id": 8,
                "name": "Task #4",
                "order": 1,
                "column": Column(id=3),
                "label": Label(id=2),
            },
        ],
    },
    {
        "table_name": Role,
        "table_dada": [
            {
                "id": 1,
                "name": "admin",
                "description": "Администратор"
            },
            {
                "id": 2,
                "name": "participant",
                "description": "Участник"
            },
            {
                "id": 3,
                "name": "guest",
                "description": "Гость"
            }

        ],
    },
    {
        "table_name": DashboardUserRole,
        "table_dada": [
            {
                "id": 1,
                "dashboard": Dashboard(id=1),
                "user": User(id=5),
                "role": Role(id=1),
            },
            {
                "id": 2,
                "dashboard": Dashboard(id=2),
                "user": User(id=5),
                "role": Role(id=1),
            },
            {
                "id": 3,
                "dashboard": Dashboard(id=1),
                "user": User(id=2),
                "role": Role(id=2),
            },
            {
                "id": 4,
                "dashboard": Dashboard(id=2),
                "user": User(id=4),
                "role": Role(id=2),
            },
        ],
    },
]

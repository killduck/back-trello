from trello.models import Column, Card, Person, Dashboard

tables = [
    {
        "table_name": Dashboard,
        "table_dada": [
            {"id": 1, "name": "diplom", "img": ""},
            {"id": 2, "name": "test_dashboard", "img": ""},
        ],
    },
    {
        "table_name": Column,
        "table_dada": [
            {
                "id": 1,
                "name":
                "backlog",
                "order": 0,
                "dashboard": Dashboard(id=1)
            },
            {
                "id": 2,
                "name": "in progress",
                "order": 1,
                "dashboard": Dashboard(id=1),
            },
            {
                "id": 3,
                "name": "test_1",
                "order": 1,
                "dashboard": Dashboard(id=2),
            },
            {
                "id": 4,
                "name": "test_2",
                "order": 0,
                "dashboard": Dashboard(id=2),
            },
        ],
    },
    {
        "table_name": Person,
        "table_dada": [
            {
                "id": 1,
                "first_name": "Андрей",
                "last_name": "Рубцов",
                "nick_name": "Raa78",
            },
            {
                "id": 2,
                "first_name": "Илья",
                "last_name": "Полетуев",
                "nick_name": "ilya616",
            },
            {
                "id": 3,
                "first_name": "Леонид",
                "last_name": "Кильдюшев",
                "nick_name": "killduck",
            },
        ],
    },
    {
        "table_name": Card,
        "table_dada": [
            {
                "id": 1,
                "name": "Максим es lint",
                "author": Person(id=3),
                "order": 3,
                "column": Column(id=1),
            },
            {
                "id": 2,
                "name": "Лёня хреначит реакт компоненты",
                "author": Person(id=1),
                "order": 2,
                "column": Column(id=1),
            },
            {
                "id": 3,
                "name": "Кнопки меню",
                "author": Person(id=2),
                "order": 1,
                "column": Column(id=2),
            },
            {
                "id": 4,
                "name": "Task 1",
                "author": Person(id=1),
                "order": 0,
                "column": Column(id=3),
            },
            {
                "id": 5,
                "name": "Task 2",
                "author": Person(id=3),
                "order": 1,
                "column": Column(id=4),
            },
        ],
    },
]

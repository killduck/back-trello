from trello.models import Column, Card, Person, Dashboard

tables = [
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
                "name": "ES Lint",
                "author": Person(id=3),
                "order": 0,
                "column": Column(id=1),
            },
            {
                "id": 2,
                "name": "Лёня хреначит реакт компоненты",
                "author": Person(id=3),
                "order": 1,
                "column": Column(id=1),
            },
            {
                "id": 3,
                "name": "Task #1",
                "author": Person(id=1),
                "order": 0 ,
                "column": Column(id=2),
            },
            {
                "id": 4,
                "name": "Task #2",
                "author": Person(id=3),
                "order": 1 ,
                "column": Column(id=2),
            },
            {
                "id": 5,
                "name": "Кнопки меню",
                "author": Person(id=2),
                "order": 0,
                "column": Column(id=4),
            },
                        {
                "id": 6,
                "name": "Search button",
                "author": Person(id=1),
                "order": 1,
                "column": Column(id=4),
            },
            {
                "id": 7,
                "name": "Task #3",
                "author": Person(id=3),
                "order": 0 ,
                "column": Column(id=3),
            },
            {
                "id": 8,
                "name": "Task #4",
                "author": Person(id=1),
                "order": 1 ,
                "column": Column(id=3),
            },
        ],
    },
]

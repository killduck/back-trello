from trello.models import (
    Columns,
    Cards,
)


tables = [
    {
        'table_name': Columns,
        'table_dada': [
            {
                "id": 1,
                "name": "backlog",
                "order": 1,
            },
            {
                "id": 2,
                "name": "in progress",
                "order": 2,
            },
        ],
    },
    {
        'table_name': Cards,
        'table_dada': [
            {
                "id": 1,
                "name": "Максим es lint",
                "author_id": 3,
                "order": 1,
                'columns': Columns(id=1)
            },
            {
                "id": 2,
                "name": "Лёня хреначит реакт компоненты",
                "author_id": 2,
                "order": 2,
                'footer_menu': Columns(id=1)
            },
            {
                "id": 3,
                "name": "Кнопки меню",
                "author_id": 4,
                "order": 1,
                'footer_menu': Columns(id=2)
            },
        ],
    },
]

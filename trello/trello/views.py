from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET", "POST", "PUT"])
def test(request):
    return Response(
        [
            {
                "id": 1,
                "name": "backlog",
                "order": 1,
                "cards": [
                    {
                        "id": 1,
                        "name": "Максим es lint",
                        "author_id": 3,
                        "order": 1,
                    },
                    {
                        "id": 2,
                        "name": "Лёня хреначит реакт компоненты",
                        "author_id": 2,
                        "order": 2,
                    },
                ],
            },
            {
                "id": 2,
                "name": "in progress",
                "order": 2,
                "cards": [
                    {
                        "id": 3,
                        "name": "Кнопки меню",
                        "author_id": 4,
                        "order": 1,
                    }
                ],
            },
        ]
    )

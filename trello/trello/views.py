from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Card, Column, Person
from .serializers import CardSerializer, ColumnSerializer, PersonSerializer

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

@api_view(["GET",])
def columns(request):
    queryset = Column.objects.all()
    serializer = ColumnSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["GET", "POST",])
def columns_edite(request):
    if request.method == 'POST':
        serializer = ColumnSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    queryset = Column.objects.all()
    serializer = ColumnSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["GET", "POST",])
def cards(request):
    if request.method == 'POST':
        serializer = CardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    queryset = Card.objects.all()
    serializer = CardSerializer(queryset, many=True)
    return Response(serializer.data)

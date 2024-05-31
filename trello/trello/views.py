from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Card, Column, Person
from .serializers import CardSerializer, ColumnSerializer, PersonSerializer


# @api_view(["GET", "POST", "PUT"])
# def test(request):
#     return Response(
#         [
#             {
#                 "id": 1,
#                 "name": "backlog",
#                 "order": 1,
#                 "cards": [
#                     {
#                         "id": 1,
#                         "name": "Максим es lint",
#                         "author_id": 3,
#                         "order": 1,
#                     },
#                     {
#                         "id": 2,
#                         "name": "Лёня хреначит реакт компоненты",
#                         "author_id": 2,
#                         "order": 2,
#                     },
#                 ],
#             },
#             {
#                 "id": 2,
#                 "name": "in progress",
#                 "order": 2,
#                 "cards": [
#                     {
#                         "id": 3,
#                         "name": "Кнопки меню",
#                         "author_id": 4,
#                         "order": 1,
#                     }
#                 ],
#             },
#         ]
#     )


def change_order_columns(request, columns_db):
    # очистка в таблице Column полей "order" для перезаписи
    for column_db in columns_db:
        column_db.order = None
        column_db.save(update_fields=["order"])

    for column in request.data:
        for column_db in columns_db:
            if column_db.id == column["id"] and column_db.name == column["name"]:
                column_db.order = column["order"]
                column_db.save(update_fields=["order"])

    # создаём новые порядковые номера для колонок
    # serial = 0
    # for column in request.data:
    #     column["order"] = serial
    #     try:
    #         # перезаписываем в БД для соответствующих колонок поля "order"
    #         for column_db in columns_db:
    #             if column_db.id == column["id"] and column_db.name == column["name"]:
    #                 column_db.order = column["order"]
    #                 column_db.save(update_fields=["order"])
    #     except Exception as error:
    #         print(f"{error} _Нет такой колонки;")
    #     serial += 1


def create_new_column(request, columns_db):
    ids = []
    orders = []
    new_data = {}
    # собираем все "id" и "order" из DB
    for column_db in columns_db:
        ids.append(column_db.id)
        orders.append(column_db.order)
    # записываем новые данные для новой колонки
    for column_req in request.data:
        if column_req["id"] not in ids:
            new_data = {
                "id": max(ids) + 1,
                "name": column_req["name"],
                "order": max(orders) + 1,
            }
    return new_data


@api_view(["GET"])
def columns(request):

    if request.method == "POST":
        columns_db = Column.objects.all()
        # print(len(columns_db))
        # print(len(request.data))
        print(request.data)
        if len(columns_db) == len(request.data):
            change_order_columns(request, columns_db)
            print("обновили порядок колонок в БД")

        elif len(columns_db) > len(request.data):
            print("была удаленна колонка и нужно обновить БД")

        elif len(columns_db) < len(request.data):
            # проверяем и готовим данные для колонки перед записью в БД
            new_data = create_new_column(request, columns_db)
            # добавляем колонку в БД
            Column.objects.create(
                id=new_data["id"],
                name=new_data["name"],
                order=new_data["order"],
            )
            print("была добавлена колонка и нужно обновить БД")

        else:
            print("если что-то сюда прилетит, то будем разбираться")

    queryset = Column.objects.all()
    serializer = ColumnSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def edite_columns(request):
    columns_db = Column.objects.all()

    print(request.data)
    if len(columns_db) == len(request.data):
        change_order_columns(request, columns_db)
        print("обновили порядок колонок в БД")

    elif len(columns_db) > len(request.data):
        print("была удаленна колонка и нужно обновить БД")

    elif len(columns_db) < len(request.data):
        # проверяем и готовим данные для колонки перед записью в БД
        new_data = create_new_column(request, columns_db)
        # добавляем колонку в БД
        Column.objects.create(
            id=new_data["id"],
            name=new_data["name"],
            order=new_data["order"],
        )
        print("была добавлена колонка и нужно обновить БД")

    else:
        print("если что-то сюда прилетит, то будем разбираться")

    queryset = Column.objects.all()
    serializer = ColumnSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(
    [
        "GET",
        "POST",
    ]
)
def columns_edite(request):
    if request.method == "POST":
        serializer = ColumnSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    queryset = Column.objects.all()
    print(queryset)
    serializer = ColumnSerializer(queryset, many=True)
    print(serializer)
    return Response(serializer.data)


@api_view(
    [
        "GET",
        "POST",
    ]
)
def cards(request):
    if request.method == "POST":
        serializer = CardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    queryset = Card.objects.all()
    serializer = CardSerializer(queryset, many=True)
    return Response(serializer.data)

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Card, Column, Person
from .serializers import CardSerializer, ColumnSerializer, PersonSerializer
from .views_functions.column_functions import change_order_columns, check_new_column


@api_view(["GET"])
def columns(request):
    queryset = Column.objects.all()
    serializer = ColumnSerializer(queryset, many=True)
    return Response(serializer.data)


# Версия Леонида, коментируем до лучших времен
# @api_view(["POST"])
# def create_columns(request):
#     columns_db = Column.objects.all()

#     if len(columns_db) < len(request.data):
#         # проверяем и готовим данные для колонки перед записью в БД
#         new_data = check_new_column(request, columns_db)
#         # добавляем колонку в БД
#         Column.objects.create(
#             id=new_data["id"],
#             name=new_data["name"],
#             order=new_data["order"],
#         )
#         print("добавлена колонка в БД")
#     else:
#         print("если что-то сюда прилетит, то будем разбираться")

#     queryset = Column.objects.all()
#     serializer = ColumnSerializer(queryset, many=True)
#     return Response(serializer.data)


# Версия Андрея, как временное решение - но вроде рабочее
@api_view(["GET", "POST"])
def create_columns(request):
    print('create_columns=>', request.data)
    try:
        Column.objects.create(
            name=request.data["name"],
            order=request.data["order"],
        )
        print("добавлена колонка в БД")
    except:
        print("писец колонка не добавлена")


    queryset = Column.objects.all()
    serializer = ColumnSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def swap_columns(request):
    columns_db = Column.objects.all()
    # print(request.data)
    if len(columns_db) == len(request.data):
        change_order_columns(request, columns_db)
        print("обновили порядок колонок в БД")
    else:
        print("если что-то сюда прилетит, то будем разбираться")

    queryset = Column.objects.all()
    serializer = ColumnSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def delete_columns(request):
    columns_db = Column.objects.all()

    if len(columns_db) > len(request.data):
        # тут нужен код для удаления колонки !!!
        print("была удаленна колонка и нужно обновить БД")
    else:
        print("если что-то сюда прилетит, то будем разбираться")

    queryset = Column.objects.all()
    serializer = ColumnSerializer(queryset, many=True)
    return Response(serializer.data)


# @api_view(["GET", "POST",])
# def columns_edite(request):
#     if request.method == "POST":
#         serializer = ColumnSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     queryset = Column.objects.all()
#     print(queryset)
#     serializer = ColumnSerializer(queryset, many=True)
#     print(serializer)
#     return Response(serializer.data)


@api_view(["GET", "POST",])
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

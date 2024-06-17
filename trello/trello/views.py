from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Card, Column, Person, Dashboard
from .serializers import CardSerializer, ColumnSerializer, PersonSerializer
from .views_functions.column_functions import change_order_columns


@api_view(["GET"])
def columns(request):
    queryset = Column.objects.all()
    serializer = ColumnSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def dashboards(request):
    queryset = Dashboard.objects.all()
    serializer = ColumnSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def swap_columns(request):
    columns_db = Column.objects.all()

    if len(columns_db) == len(request.data):
        change_order_columns(request, columns_db)
        print("обновили порядок колонок в БД")
    else:
        print("если что-то сюда прилетит, то будем разбираться")

    queryset = Column.objects.all()
    serializer = ColumnSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["GET", "POST"])
def create_column(request):
    print('create_column(request)=>', request.data)
    # TODO добавить параметры idWorkSpace: 1, idDashboard: 1

    last_column_order = Column.objects.all().last()

    try:
        new_add_column = Column.objects.create(
            name=request.data['nameNewColumn'],
            order=last_column_order.order + 1 if last_column_order else 0,
            dashboard_id = request.data['idDashboard'],
        )
        print("добавлена колонка в БД")
        serializer = ColumnSerializer(new_add_column)
        return Response(serializer.data)
    except:
        return Response(False, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
def delete_column(request):

    id_column_deleted = request.data["id_column"]

    try:
        Column.objects.filter(id=id_column_deleted).delete()
        return Response(True, status=status.HTTP_200_OK)
    except:
        return Response(False, status=status.HTTP_404_NOT_FOUND)


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


@api_view(["GET", "POST"])
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

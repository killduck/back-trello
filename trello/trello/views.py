from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Card, Column, Person, Dashboard
from .serializers import (
    CardSerializer,
    ColumnSerializer,
    PersonSerializer,
    DashboardSerializer,
)
from .views_functions.column_functions import change_order_columns


@api_view(["GET", "POST"])
def columns(request):

    dashboard_id = request.data["dashboardId"]

    queryset = Column.objects.all().filter(dashboard=dashboard_id)
    serializer = ColumnSerializer(queryset, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def dashboards(request):

    queryset = Dashboard.objects.all()
    serializer = DashboardSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def login(request):
    return Response(request.data)


@api_view(["POST"])
def swap_columns(request):

    dashboard_id = request.data["dashboardId"]

    try:
        for column in request.data["columns"]:
            Column.objects.filter(id=column["id"]).update(order=column["order"])
        print("обновили порядок колонок в БД")
    except:
        print("если что-то сюда прилетит, то будем разбираться")
        return Response(False, status=status.HTTP_404_NOT_FOUND)

    queryset = Column.objects.filter(dashboard=dashboard_id)
    serializer = ColumnSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def swap_cards(request):

    try:
        for card in request.data["order_cards"]:
            Card.objects.filter(id=card["id"]).update(
                order=card["order"], column=card["column"]
            )
        print("обновили порядок карточек в БД")
    except:
        print("если что-то сюда прилетит, то будем разбираться")
        return Response(False, status=status.HTTP_404_NOT_FOUND)

    dashboard_id = request.data["dashboardId"]

    list_column = Column.objects.filter(dashboard=dashboard_id)

    queryset = Card.objects.filter(column_id__in=list_column)
    serializer = CardSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["GET", "POST"])
def create_column(request):
    # TODO добавить параметры idWorkSpace: 1

    dashboard_columns = request.data["idDashboard"]

    last_column_order = Column.objects.filter(dashboard=dashboard_columns).last()

    if last_column_order:
        order = last_column_order.order + 1
    else:
        order = 0

    try:
        new_add_column = Column.objects.create(
            name=request.data["nameNewColumn"],
            order=order,
            dashboard_id=request.data["idDashboard"],
        )
    except:
        return Response(False, status=status.HTTP_404_NOT_FOUND)

    serializer = ColumnSerializer(new_add_column)
    return Response(serializer.data)


@api_view(["GET", "POST"])
def create_card(request):

    card_column = request.data["column"]

    last_card_in_column = Card.objects.filter(column=card_column).last()

    if last_card_in_column:
        order = last_card_in_column.order + 1
    else:
        order = 0

    try:
        new_add_card = Card.objects.create(
            name=request.data["name"],
            author_id=request.data["author"],
            order=order,
            column_id=request.data["column"],
        )

    except:
        return Response(False, status=status.HTTP_404_NOT_FOUND)

    serializer = CardSerializer(new_add_card)
    return Response(serializer.data)


@api_view(["POST"])
def delete_column(request):

    id_column_deleted = request.data["id_column"]

    try:
        Column.objects.filter(id=id_column_deleted).delete()
    except:
        return Response(False, status=status.HTTP_404_NOT_FOUND)

    return Response(True, status=status.HTTP_200_OK)


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

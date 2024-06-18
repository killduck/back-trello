# sorry!, функция во вьюхе больше не используется
def change_order_columns(request, columns_db):
    # очистка в таблице Column полей "order" для перезаписи
    for column_db in columns_db:
        column_db.order = None
        column_db.save(update_fields=["order"])

    # перезаписываем в БД для соответствующих колонок поля "order"
    for column in request.data:
        for column_db in columns_db:
            if column_db.id == column["id"] and column_db.name == column["name"]:
                column_db.order = column["order"]
                column_db.save(update_fields=["order"])


# sorry!, функция во вьюхе больше не используется
def check_new_column(request, columns_db):
    ids = []
    orders = []
    new_data = {}
    # собираем все "id" и "order" из DB
    if len(columns_db) > 0:
        for column_db in columns_db:
            ids.append(column_db.id)
            orders.append(column_db.order)
        # записываем новые данные для новой колонки
        for column_req in request.data:
            if ((column_req["id"] not in ids) and
                    ((max(ids)+1) == column_req["id"]) and
                    ((max(orders)+1) == column_req["order"])):
                new_data = {
                    "id": max(ids) + 1,
                    "name": column_req["name"],
                    "order": max(orders) + 1,
                }
    else:
        for column_req in request.data:
            if column_req["id"] == 1 and column_req["order"] == 1:
                new_data = {
                    "id": column_req["id"],
                    "name": column_req["name"],
                    "order": column_req["order"],
                }
    return new_data

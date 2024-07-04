from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand

from django_seed import Seed

from trello.management.seed import trello_fake_db as db
from trello.models import User


class Command(BaseCommand):
    _tables = db.tables

    def handle(self, *args, **options):
        # очистка и запись служебной таблицы
        try:
            if type(self._tables) is list and len(self._tables) != 0:
                flag = False
                for table in self._tables:
                    if len(table['table_name'].objects.all()) != 0:
                        TableClearing(table['table_name'])
                    flag = self._write_data_to_table(table['table_name'], table['table_dada'])
                    flag = self._write_password_to_user(table['table_name'], table['table_dada'])
                if flag:
                    print('seeds_(answer): Файлы добавлены в БД.')
                else:
                    print('seeds_(answer): Ошибка работы в файлами.')
            else:
                self._table_type_error()

        except Exception as err:
            print(err)

    def _table_type_error(self):
        if list is not type(self._tables):
            print(f'seeds_(answer): file _tables: {self._tables}, is not "list". it`s: {type(self._tables)}.')
        elif len(self._tables) == 0:
            print(f'seeds_(answer): the file _tables: {self._tables} is a list, but it is empty.')
        else:
            print('seeds_(answer): wtf...')

    @staticmethod
    def _write_data_to_table(table_name, table_dada):
        seeder = Seed.seeder()
        for data_element in table_dada:
            seeder.add_entity(table_name, 1, data_element)
        seeder.execute()
        return True

    @staticmethod
    def _write_password_to_user(table_name, table_dada):
        if table_name.__name__ == "User":
            for user in table_dada:
                password_from_db = make_password(user['password'], salt=None, hasher='default')
                print('last_login>>>', user['last_login'], 'type>>>', type(user['last_login']))
                User.objects.filter(id=user["id"]).update(password=password_from_db)
        return True


class TableClearing:
    def __init__(self, table):
        table.objects.all().delete()

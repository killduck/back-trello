
from django.core.management.base import BaseCommand
from trello.management.seed import trello_fake_db as db


class Command(BaseCommand):
    _tables = db.tables

    def handle(self, *args, **options):
        if type(self._tables) is list and len(self._tables) != 0:
            flag = False
            for table in self._tables:
                table['table_name'].objects.all().delete()
                if len(table['table_name'].objects.all()) != 0:
                    flag = False
                    break
                flag = True
            if flag:
                print('clear_DB_(answer): Файлы таблиц в БД очищены.')
            else:
                print('clear_DB_(answer): Таблица не очищена.')
        else:
            self._table_type_error()

    def _table_type_error(self):
        if list is not type(self._tables):
            print(f'clear_DB_(answer): file _tables: {self._tables}, is not "list". it`s: {type(self._tables)}.')
        elif len(self._tables) == 0:
            print(f'clear_DB_(answer): the file _tables: {self._tables} is a list, but it is empty.')
        else:
            print('clear_DB_(answer): wtf...')

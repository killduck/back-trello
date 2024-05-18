from django.core.management.base import BaseCommand
from django_seed import Seed

from trello.management.seed import columns_cards_db as db


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
                if flag:
                    print('seedsAnswer: Files are uploaded to the DB.')
                else:
                    print('seedsAnswer: Files loading error.')
            else:
                self._table_type_error()

        except Exception as err:
            print(err)

    def _table_type_error(self):
        if list != type(self._tables):
            print(f'seedsAnswer: file _tables: {self._tables}, is not "list". it`s: {type(self._tables)}.')
        elif len(self._tables) == 0:
            print(f'seedsAnswer: the file _tables: {self._tables} is a list, but it is empty.')
        else:
            print('seedsAnswer: wtf...')

    def _write_data_to_table(self, table_name, table_dada):
        seeder = Seed.seeder()
        for data_element in table_dada:
            seeder.add_entity(table_name, 1, data_element)
        seeder.execute()
        return True


class TableClearing:
    def __init__(self, table):
        table.objects.all().delete()

from django.core.management.base import BaseCommand
from django_seed import Seed

from trello.management.seed import columns_cards_db as db
gi

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
                self._tableTypeError()

        except Exception as err:
            print(err)

    def _tableTypeError(self):
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
            # print('В модель =', table_name.__name__, 'загружены данные =', data_element)
        seeder.execute()
        return True


class TableClearing:
    def __init__(self, table):
        table.objects.all().delete()

# 'допилил команду "seeds" V2'
# расширенная версия
'''
from django.core.management.base import BaseCommand
from django_seed import Seed
from magazin.models import FooterMenu, FooterMenuItems
# таблица в папке seed в файле footer_menu_db
from magazin.management.seed import footer_menu_db


class Command(BaseCommand):
    _id = None
    _tables = footer_menu_db.tables

    def handle(self, *args, **options):
        # очистка и запись служебной таблицы
        try:
            if self._tables is not None:
                for table in self._tables:
                    if len(table['table_name'][0].objects.all()) != 0:
                        TableClearing(table['table_name'][0])
                    self._write_data_to_table(table['table_name'], table['table_dada'])

        except Exception as err:
            print(err)

    # тут записываем данные в БД
    def _write_data_to_table(self, table_name, table_dada):
        seeder = Seed.seeder()
        for data_element in table_dada:
            seeder.add_entity(table_name[0], 1, data_element)
        seeder.execute()
        # проверка наличия FKey
        if table_name[1] == 'FKey':
            self.insert_foreign_key()

    # тут делаем общие ключи
    def made_foreign_keys(self):
        foreign_keys = {}
        key = 1
        for field in FooterMenu.objects.all():
            if field.id == key:
                foreign_keys[f"new_id_{key}"] = field
                key = key + 1
        return foreign_keys

    # тут делаем в 'made_foreign_keys' и вставляем общие ключи
    def insert_foreign_key(self):
        target_key = self.made_foreign_keys()

        for field in FooterMenuItems.objects.all():
            if 0 < field.id < 7:
                field.footer_menu = target_key['new_id_1']
                field.save(update_fields=['footer_menu'])
            else:
                # field.footer_menu = target_key['new_id_2']
                # field.save(update_fields=['footer_menu'])


class TableClearing:
    def __init__(self, table):
        table.objects.all().delete()
'''

'''
114__ FooterMenu object (1)
# new_id = FooterMenu.objects.get(id=1)
# print(field.footer_menu) # print(new_id.name) # field.footer_menu = new_id
# кидает ошибку при field.footer_menu = 1
# ValueError: Cannot assign "1": "FooterMenuItems.footer_menu" must be a "FooterMenu" instance.
# print(f'103__ {FooterMenuItems.objects.get(id=1).footer_menu}')
'''

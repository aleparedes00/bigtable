import os
from datetime import datetime

from google.cloud import bigtable
from google.cloud.bigtable import column_family

os.environ["BIGTABLE_EMULATOR_HOST"] = 'localhost:8086'

INSTANCE_NAME = 'instance1'
TABLE_NAME = 'booking'
columns_hotel = ['hotel_name', 'garage', 'baby_bed', 'breakfast', 'couple_combo']
columns_reservation = ['user_id', 'reservation_id', 'price']
CLIENT = bigtable.Client(project='api-booking-235813', admin=True)
INSTANCE = CLIENT.instance(INSTANCE_NAME)
COLUMN_FAMILY_ID_LIST = ['_hotel', '_reservation']


def get_table():
    table = INSTANCE.table(table_id=TABLE_NAME)

    # Create Rules for Garbage Collector. After 2 versions of data_cell, the oldest is dismissed
    max_versions_rule = column_family.MaxVersionsGCRule(2)

    # Columns families & Columns names
    columns_family_id = ['_hotel', '_reservation']
    column_families = {columns_family_id[0]: max_versions_rule,
                       columns_family_id[1]: max_versions_rule}
    if not table.exists():
        table.create(column_families=column_families)
        cf = table.list_column_families()
        print('table: {} has been created\nwith columns familes: {}, {}'.
              format(TABLE_NAME, cf.get('_hotel'), cf.get('_reservation')))
    return table


def create_key_row(room_id: str, reservation_date: datetime):
    date_epoch = reservation_date.timestamp()
    return '{}#{}'.format(room_id, str(int(date_epoch)))


def insert_new_row(row_key: str, column: str, value: str, column_family: str):
    column = column.encode()
    value_b = value.encode()
    row = get_table().row(row_key)
    row.set_cell(column_family_id=column_family, column=column, value=value_b)
    get_table().mutate_rows([row])


def insert_row(data: dict, key: str, column_families: list):
    # TODO pass only data to be inserted controller
    _hotel = ['hotel_name', 'garage', 'baby_bed', 'breakfast', 'couple_combo']
    row = get_table().row(key)
    for k, v in data.items():
        row.set_cell()
        print('column name: {}, cell value: {}'.format(k, v))

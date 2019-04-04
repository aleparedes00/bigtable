import os
from datetime import datetime

from google.cloud import bigtable
from google.cloud.bigtable import column_family

from src import config

os.environ["BIGTABLE_EMULATOR_HOST"] = 'localhost:8086'

CLIENT = bigtable.Client(project='api-booking-235813', admin=True)
INSTANCE = CLIENT.instance(config.INSTANCE_NAME)



def insert_new_row(row_key: str, column: str, value: str, column_family: str):
    column = column.encode()
    value_b = value.encode()
    row = get_table().row(row_key)
    row.set_cell(column_family_id=column_family, column=column, value=value_b)
    get_table().mutate_rows([row])


def insert_row(data: dict, key: str):
    # TODO pass only data to be inserted controller
    _hotel = ['hotel_name', 'garage', 'baby_bed', 'breakfast', 'couple_combo']
    _reservation = ['user_id', 'reservation_id', 'price']
    row = get_table().row(key)
    for k, v in data.items():
        if k in _hotel:
            column_family_id = '_hotel'
        else:
            column_family_id = '_reservation'
        if type(v) == datetime:
            continue
        column = k.encode()
        value = v.encode()
        row.set_cell(column_family_id=column_family_id, column=column, value=value)
        # row.append_cell_value(column_family_id=column_family_id, column=column, value=value)
    # get_table().mutate_rows(row)
    row.commit()
    row.clear()


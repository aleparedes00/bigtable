import os

from google.cloud import bigtable
from google.cloud.bigtable import column_family

from src import config

os.environ["BIGTABLE_EMULATOR_HOST"] = 'localhost:8086'

CLIENT = bigtable.Client(project='api-booking-235813', admin=True)
INSTANCE = CLIENT.instance(config.INSTANCE_NAME)


def get_table():
    table = INSTANCE.table(table_id=config.TABLE_NAME)

    # Create Rules for Garbage Collector. After 2 versions of data_cell, the oldest is dismissed
    max_versions_rule = column_family.MaxVersionsGCRule(2)

    # Columns families & Columns names
    column_families = {config.COLUMN_FAMILY_ID_LIST[0]: max_versions_rule,
                       config.COLUMN_FAMILY_ID_LIST[1]: max_versions_rule}
    if not table.exists():
        table.create(column_families=column_families)
        cf = table.list_column_families()
        print('table: {} has been created\nwith columns familes: {}, {}'.
              format(config.TABLE_NAME, cf.get('_hotel'), cf.get('_reservation')))
    return table


""""
######################## READ ########################
"""


def keys_exist(key_list: list) -> bool:
    """
    Check if row exists for a given key
    :param key_list: list of keys(room_id#epoch)
    :return: boolean True=Reservation Exist
    """
    for k in key_list:
        row_data = get_table().read_row(k)
        if row_data:
            return True
    return False


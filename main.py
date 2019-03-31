from datetime import datetime

from google.cloud.bigtable import row_filters

# The client must be created with admin=True because it will create a
# table.
from create import create_key_row, insert_new_row, insert_row
from read import read_row


def reservation_example():
    _dict = dict
    # _dict = 'room_ids': 'e1eb64f7-c4f5-43b5-b114-eddb4458ee60',
    return { 'room_id': 'd5f457c6-4533-4838-831d-ebc80abc89e8',
             'date_start': datetime(2019, 6, 20, 0, 0),
             'date_end': datetime(2019, 6, 25, 0, 0),
             'hotel_name': 'hotel1',
             'user_id': '6979d1ee-03bc-4f23-bcfd-cefd0461e4a5',
             'garage': True,
             'baby_bed': True}


def read_one_row(table, column_family_id, column, key: bytes):
    row_filter = row_filters.CellsColumnLimitFilter(1)
    print(key)
    row = table.read_row(key, row_filter)
    cell = row.cells[column_family_id][column][0]
    return cell.value.decode('utf-8')


def writing_cbt(table, column_family_id):
    print('Writing some greetings to the table.')
    greetings = ['Hello World!', 'Hello Cloud Bigtable!', 'Hello Python!']
    rows = []
    column = 'greeting'.encode()
    for i, value in enumerate(greetings):
        # Note: This example uses sequential numeric IDs for simplicity,
        # but this can result in poor performance in a production
        # application.  Since rows are stored in sorted order by key,
        # sequential keys can result in poor distribution of operations
        # across nodes.
        #
        # For more information about how to design a Bigtable schema for
        # the best performance, see the documentation:
        #
        row_key = 'greeting{}'.format(i).encode()
        print(row_key)
        row = table.row(row_key)
        row.set_cell(column_family_id,
                     column,
                     value,
                     timestamp=datetime.utcnow())
        rows.append(row)
    table.mutate_rows(rows)


def main():
    # table = create_table()
    # cf = table.list_column_families()
    # column_family_obj_h = cf['_hotel']
    # column_family_obj_r = cf['_reservation']
    # print('table: {} has been created\nwith columns familes: {}, {}'.
    #       format('booking', column_family_obj_h.name, column_family_obj_r.name))
    example_dict = reservation_example()
    key = create_key_row(example_dict.get('room_id'), example_dict.get('date_start'))
    print(key)
    column = 'hotel_name'
    column_family_id = '_hotel'
    value = example_dict.get('hotel_name')
    # insert_new_row(key, column=column, value=value, column_family=column_family_id)
    # read_row(key, column_family_id, column)
    insert_row(example_dict, key)


if __name__ == '__main__':
    main()

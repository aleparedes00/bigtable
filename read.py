from create import get_table


def read_row(key, column_family_id, column):
    row = get_table().read_row(key)
    encodedColumn = column.encode()
    cell = row.cells[column_family_id][encodedColumn]
    print(cell.value.decode('utf-8'))

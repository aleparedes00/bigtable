from src.cbt_repository import get_table


def read_rows(data, key):
    # for row in get_table().read_rows():
    #     print(row.cells[column_family][column.encode()][0].decode('UTF-8'))
    row_data = get_table().read_row(key)
    for k, v in data.items():
        print("On column_family {}".format(k))
        for e in v:
            try:
                cell = row_data.cells[k][e.encode()][0]
                print("for column {} value {}".format(e, cell.value.decode()))
            except KeyError:
                print('exception')
    # for cell in cells:
    #     print(cell.value.decode())
    return True

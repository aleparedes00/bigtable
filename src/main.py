from datetime import datetime

import connexion

# The client must be created with admin=True because it will create a
# table.

from read import read_rows
from src import mocks
from src.api.v1.reservation.controller import try_reservation, create_date_list


def reservation_example():
    _dict = dict
    # _dict = 'room_ids': 'e1eb64f7-c4f5-43b5-b114-eddb4458ee60',
    return {'room_id': 'd5f457c6-4533-4838-831d-ebc80abc89e8',
             'date_start': datetime(2019, 6, 20, 0, 0),
             'date_end': datetime(2019, 6, 25, 0, 0),
             'hotel_name': 'hotel1',
             'user_id': '6979d1ee-03bc-4f23-bcfd-cefd0461e4a5',
             'garage': 'True',
             'baby_bed': 'True'}


app = connexion.App(__name__, specification_dir='openapi/')
app.add_api('booking_api.yaml', base_path='/api')

# res = try_reservation(date_list=mocks.DATES, rooms_id=mocks.ROOMS_ID)
res = create_date_list(date_end=mocks.DATES[0],date_start= mocks.DATES[2])
print(res)


if __name__ == '__main__':
    app.run(port=8080)


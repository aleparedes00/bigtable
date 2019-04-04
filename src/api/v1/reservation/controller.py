# TODO separate dates into single date list
# TODO check if key exists
import uuid
import datetime

from src import config, mocks
from src.cbt_repository import keys_exist
from src.cbt_repository.tools import create_key_row


def split_data_to_insert(data: {}):
    # Split data depending column family and columns
    # TODO to be continued some data is already inside the table
    split_data = {'_hotel': {}, '_reservation': {}}
    for k, v in data.items():
        if k in config.columns_hotel:
            split_data["_hotel"].update({k: v})
        if k in config.columns_reservation:
            split_data['_reservation'].update({k: v})
    split_data['key'] = {data.get('room_id')}
    pass


def try_reservation(date_list: list, rooms_id: list):
    key_list = []
    _format = '%Y %m %d'
    for _id in rooms_id:
        for date in date_list:
            _date_obj = datetime.datetime.strptime(date, _format)
            _key = create_key_row(_id, _date_obj)
            key_list.append(_key)
        room_occupied = keys_exist(key_list)
        if not room_occupied:
            # Create a reservation_id
            reservation_id = str(uuid.uuid1()).replace('-', '')

            return "coucou"
    return 'Dates not availables', 301


def create_date_list(date_start, date_end):
    _format = '%Y %m %d'
    _date_start = datetime.datetime.strptime(date_start, _format)
    _date_end = datetime.datetime.strptime(date_end, _format)
    nb_days = (_date_end - _date_start).days
    _list = [_date_start + datetime.timedelta(days=d) for d in range(0, nb_days, 1)]
    return _list

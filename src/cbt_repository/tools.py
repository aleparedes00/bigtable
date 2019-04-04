from datetime import datetime


def create_key_row(room_id: str, reservation_date: datetime) -> str:
    """
    Create the key for CBT
    :type reservation_date: datetime
    :param room_id: id of the room for the reservation
    :return str room_id#epoch(reservation_date)
    """
    date_epoch = reservation_date.timestamp()
    return '{}#{}'.format(room_id, str(int(date_epoch)))

from data.connection import ConnectionRepository
from domain.model import WSConnection

repo = ConnectionRepository()


def get_connections_by_room(room_id: str):
    return repo.get_by_room_id(room_id)


def create_connection(data):
    wid = repo.create(WSConnection(**data))
    return wid


def delete_connection(connection_id):
    res = repo.delete(connection_id)
    return res




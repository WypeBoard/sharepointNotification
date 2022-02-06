from typing import List

from connector import DbConnector
from model.physical.Notification import Notification


def _update_entity(notification: Notification):
    query = 'UPDATE NOTIFICATION SET CASE_ID = ?,CASE_TITLE = ?, STATUS = ?, NEXT_NOTIFICATION = ?, AENDRET = ?, AENDRET_AF = ? WHERE ID = ?'
    params = (notification.case_id, notification.case_title, notification.status.name, notification.next_notification,
              notification.aendret, notification.aendret_af, notification.id)
    return DbConnector.persist_entity(query, params)


def _new_entity(notification: Notification):
    query = 'INSERT INTO NOTIFICATION (ID, CASE_ID, CASE_TITLE, STATUS, NEXT_NOTIFICATION, OPRETTET, OPRETTET_AF, AENDRET, AENDRET_AF) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
    params = (notification.id, notification.case_id, notification.case_title, notification.status.name, notification.next_notification,
              notification.oprettet, notification.oprettet_af, notification.aendret, notification.aendret_af)
    return DbConnector.persist_entity(query, params)


def persist_entity(notification: Notification):
    if notification.id is None:
        notification.create_new_db_entity()
        _new_entity(notification)
    else:
        notification.update_db_entity()
        _update_entity(notification)
    return notification


def get_all_entities() -> List[Notification]:
    query = 'SELECT nf.* FROM NOTIFICATION nf'
    query_result = DbConnector.fetch_entities(query, ())
    data = []
    for result in query_result:
        data.append(Notification.map_from_db(result))
    return data

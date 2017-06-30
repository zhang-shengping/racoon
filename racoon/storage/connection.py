#!/usr/bin/env python
# encoding: utf-8

import json

from oslo_config import cfg
from oslo_db.sqlalchemy import session as db_session
from oslo_log import log

from racoon import storage
from racoon.storage import models

LOG = log.getLogger(__name__)


def get_conn_from_config(conf):
    url = conf.database.connection
    return Connection(url)


class Connection(storage.BaseConnection):

    def __init__(self, url):
        opts = dict(cfg.CONF.database.items())
        self._engine_facade = db_session.EngineFacade(url, **opts)

    @property
    def engine(self):
        return self._engine_facade.get_engine()

    @property
    def session(self):
        return self._engine_facade.get_session()

    def resource_start(self, resource):

        # with session and session commit
        # both session must the same session
        # here is the session
        se = self.session

        # use for debug
        # raise Exception

        with se.begin():
            timetable = models.TimeTable(
                message_id=resource.message_id,
                resource_id=resource.resource_id,
                user_id=resource.user_id,
                project_id=resource.project_id,
                start_timestamp=resource.timestamp,
                attributes=json.dumps(resource.attributes))

            se.add(timetable)

        LOG.info('resource %s is persisted',
                 resource)

    def resource_end(self, resource):
        # TRY to find a resource in db
        # select resource_id and end_timestamp is null
        # then add a end_timestamp

        se = self.session
        try:
            pass
        except Exception:
            LOG.inf('can not found resource %s',
                    resource)

        pass

if __name__ == "__main__":
    conn = Connection(
        "mysql+pymysql://ecollector:password@localhost/ecollector")
    from racoon.storage import Resource
    session = conn.session
    # query all
    # result_set = session.query(models.TimeTable).all()
    # for re in session.query(models.TimeTable):
        # print re.resource_id

    # select the first one
    # res = session.query(models.TimeTable).first()
    # print res.resource_id

    # res = session.query(models.TimeTable).one()
    # print res.resource_id

    #res = session.query(models.TimeTable).scalar()
    #print res.resource_id

    # print(session.query(models.TimeTable.resource_id).first())
    # print(session.query(models.TimeTable.message_id).first())

    # for r in session.query(
            # models.TimeTable).order_by(
                # models.TimeTable.start_timestamp):
        # print r.start_timestamp

    from sqlalchemy import func
    a =  session.query(func.count(models.TimeTable.resource_id)).scalar()
    print a

    for i in session.query(func.count(models.TimeTable.user_id)):
        print i


    # res = {"message_id": '123213',
           # "user_id": '123213',
           # "project_id": 'tewt',
           # "attributes": 'jasdf'}

    # res = Resource(res)
    # conn.add_resource(res)


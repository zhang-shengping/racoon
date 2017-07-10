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
        _id = resource.resource_id
        timestamp = resource.timestamp

        with se.begin():
            try:
                # TODO: is there any way to make sure one record
                # and update in one query
                query = se.query(
                    models.TimeTable).filter(
                        models.TimeTable.resource_id==_id,
                        models.TimeTable.end_timestamp==None
                    ).update(
                        {models.TimeTable.end_timestamp: timestamp})

            except Exception:
                LOG.info('can set end_time to resource %s',
                        resource)
                raise

        LOG.info('resource %s sets end_timestamp <%s>',
                 resource, timestamp)

    def resource_resize(self, resource):
        # update and create should be in one transcation
        # udpate:
        # find the resource with the same id but without end_timstamp
        # then update the end_timestamp with timestamp

        # create:
        # finally create a new record start_timestamp == timestamp

        se = self.session
        _id = resource.resource_id
        timestamp = resource.timestamp

        with se.begin():
            try:
                query = se.query(
                    models.TimeTable).filter(
                        models.TimeTable.resource_id==_id,
                        models.TimeTable.end_timestamp==None
                    )
                query.update({models.TimeTable.end_timestamp: timestamp})

                timetable = models.TimeTable(
                    message_id=resource.message_id,
                    resource_id=_id,
                    user_id=resource.user_id,
                    project_id=resource.project_id,
                    start_timestamp=timestamp,
                    attributes=json.dumps(resource.attributes))

                se.add(timetable)
            except Exception:
                LOG.error('resource %s resize is not set', resource)
                raise

        LOG.info('record resource %s resize end_timestamp <%s>',
                 resource, timestamp)

    def del_resource_by_timestamp(self, timestamp):
        se = self.session

        with se.begin():
            try:
                query = se.query(
                    models.TimeTable).filter(
                        models.TimeTable.end_timestamp<=timestamp,
                        models.TimeTable.end_timestamp!=None
                    )
                query.delete()
            except Exception:
                LOG.error('can not delete resources by end_timestamp %s',
                          timestamp)
                raise

        LOG.info('delete resource by end_timestamp %s', timestamp)


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

    # from sqlalchemy import func
    # a =  session.query(func.count(models.TimeTable.resource_id)).scalar()
    # print a

    # for i in session.query(func.count(models.TimeTable.user_id).label('test'),
                           # func.count(models.TimeTable.start_timestamp)):
        # print i.keys()
        # print i.test

    # for i in session.query(
            # models.TimeTable).filter(models.TimeTable.end_timestamp != None):
        # print i

    # re = session.query(models.TimeTable).filter(
            # models.TimeTable.resource_id=="26434-480d-9c6c-4dca2309ff4b",
    # ).update({models.TimeTable.user_id: '123123123'})



    # re.update({models.TimeTable.end_timestamp: '2017-06-28 10:10:57'})
    # print re

    import datetime
    # time = datetime.datetime.utcnow() - datetime.timedelta(days=10)
    # time = time.strftime('%Y-%m-%d %H:%M:%S')
    time ='2018-07-10T06:39:16'
    LOCAL_FORMAT = '%Y-%m-%dT%H:%M:%S'
    time = datetime.datetime.strptime(time, LOCAL_FORMAT)

    re = session.query(models.TimeTable).filter(
        models.TimeTable.end_timestamp <= time
    )
    a = re.all()
    for i in a:
        print a
        print i.end_timestamp
    # res = {"message_id": '123213',
           # "user_id": '123213',
           # "project_id": 'tewt',
           # "attributes": 'jasdf'}

    # res = Resource(res)
    # conn.add_resource(res)


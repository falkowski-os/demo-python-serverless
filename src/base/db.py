import os
import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import DeclarativeMeta

from src.base.entity.base import Base


def __crete_db_session_maker():
    host = os.getenv('DB_HOST')
    user = os.getenv('DB_USER')
    pwd = os.getenv('DB_PWD')
    db_name = os.getenv('DB_NAME')
    connect_url = sqlalchemy.engine.url.URL(
        drivername='mysql+pymysql',
        username=user,
        password=pwd,
        host=host,
        port=3306,
        database=db_name)
    engine = sqlalchemy.create_engine(connect_url, echo=True)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    connection = session.connection()
    return session


def get_session():
    return __crete_db_session_maker()


class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            return fields
        return json.JSONEncoder.default(self, obj)

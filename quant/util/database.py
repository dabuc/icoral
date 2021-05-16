from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from quant.settings import QtConfig

engine = create_engine(QtConfig.DATABASE_URL)
session_factory = sessionmaker(bind=engine)


class Base(object):
    """自定义SQLAlchemy的Base基类"""

    @classmethod
    def clear_table(cls):
        """
        清空数据表
        """
        with session_scope() as sn:
            sn.query(cls).delete()


Base = declarative_base(cls=Base)


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = session_factory()
    try:
        yield session
        session.commit()
    except:  # noqa
        session.rollback()
        raise
    finally:
        session.close()
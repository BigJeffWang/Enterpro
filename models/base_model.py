import datetime
import uuid
from decimal import Decimal

from sqlalchemy import Column, BigInteger, DateTime, Boolean, INTEGER
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData
from tools.mysql_tool import MysqlTools
from utils.util import generate_order_no

Base = declarative_base()

connect_string = MysqlTools.get_connect_string()
some_engine = create_engine(connect_string, convert_unicode=True, pool_size=100)
meta = MetaData(bind=some_engine)
meta.reflect()


class BaseModel(Base):
    __abstract__ = True

    id = Column(INTEGER, primary_key=True, autoincrement=True, comment="内置索引")
    created_at = Column(DateTime, nullable=False, server_default="0000-00-00 00:00:00", comment="创建时间")
    update_at = Column(DateTime, onupdate=datetime.datetime.now, nullable=False, server_default="0000-00-00 00:00:00", comment="修改时间")
    deleted_at = Column(DateTime, nullable=False, server_default="0000-00-00 00:00:00", comment="删除时间")
    is_delete = Column(Boolean, nullable=False, default=0, server_default="0", comment="假删除 True为已删除")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.created_at = datetime.datetime.now()
        self._id = generate_order_no()

    def all_data(self):
        if "_sa_instance_state" in self.__dict__:
            self.__dict__.pop('_sa_instance_state')
        for k, v in self.__dict__.items():
            if isinstance(v, datetime.datetime):
                self.__dict__[k] = v.strftime("%Y-%m-%d %H:%M:%S")
        return self.__dict__

    def save(self, session):
        session.add(self)
        session.commit()
        return True

    def delete(self, session):
        self.deleted = True
        self.deleted_at = datetime.datetime.utcnow()
        session.commit()

    def dump_to_dict(self, args=None):
        ret = {}
        if args is None:
            args = self.__table__.columns.keys()
        for name in self.__table__.columns.keys():
            if name in args:
                if isinstance(getattr(self, name), datetime.datetime):
                    ret[name] = str(getattr(self, name))
                elif isinstance(getattr(self, name), Decimal):
                    ret[name] = float(getattr(self, name))
                else:
                    ret[name] = getattr(self, name)
        return ret

    def set_by_dict(self, args):
        keys = self.__table__.columns.keys()
        for k in args:
            if k not in keys:
                raise Exception("set a unknown key:%s" % k)
            setattr(self, k, args[k])

    @staticmethod
    def uuid():
        return uuid.uuid4().hex

    @property
    def id(self):
        return self.id

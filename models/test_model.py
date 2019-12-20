from sqlalchemy import Column, String, Numeric, DateTime, INTEGER
from models.base_model import BaseModel, meta
from utils.util import get_decimal, generate_order_no
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy import Table


class EnterpriseInfoModel(BaseModel):
    __table__ = Table('enterprise_info', meta, autoload=True)
    __tablename__ = "enterprise_info"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

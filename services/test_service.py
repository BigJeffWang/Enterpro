import random
from decimal import Decimal
import logging

from services.base_service import BaseService
from tools.mysql_tool import MysqlTools
from models.test_model import EnterpriseInfoModel


class TestService(BaseService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, params):
        """
        获取用户详情
        :param params:
        :return:
        """
        limit = int(params.get("limit") or 10)
        offset = int(params.get("offset") or 0)
        username = params.get("username")
        ret = []
        with MysqlTools().session_scope() as session:
            obj = session.query(EnterpriseInfoModel)
            if username:
                obj = obj.filter(EnterpriseInfoModel.username.like('%' + username + '%'))

            rows = obj.order_by(EnterpriseInfoModel.id.desc()).limit(limit).offset(offset).all()

            for row in rows:
                ret.append(row.all_data())
        return ret

    def post(self, params):
        """
        获取用户详情
        :param params:
        :return:
        """
        username = params.get("username")
        tel = params.get("tel")
        enterpr_name = params.get("enterpr_name")
        other = params.get("other")
        if username == "":
            return {"code": -1, "msg": "缺少必填字段"}

        with MysqlTools().session_scope() as session:
            obj = EnterpriseInfoModel(
                username=username,
                tel=tel,
                enterpr_name=enterpr_name,
                other=other
            )

            session.add(obj)
            session.commit()

        return {"code": 0, "msg": "success"}

    def patch(self, params):
        """
        修改详情
        :param params:
        :return:
        """
        _id = params.get("_id")
        username = params.get("username")
        tel = params.get("tel")
        enterpr_name = params.get("enterpr_name")
        other = params.get("other")
        if not _id:
            return {"code": -1, "msg": "缺少必填字段"}

        with MysqlTools().session_scope() as session:
            obj = session.query(EnterpriseInfoModel).filter_by(_id=_id).first()
            if not obj:
                return {"code": -1, "msg": "缺少必填字段"}
            if username:
                obj.username = username
            if tel:
                obj.tel = tel
            if enterpr_name:
                obj.enterpr_name = enterpr_name
            if other:
                obj.other = other
            session.commit()

        return {"code": 0, "msg": "success"}

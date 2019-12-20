from controllers.base_controller import BaseController
from config import get_config, get_env
from tools.mysql_tool import MysqlTools
from utils.util import get_decimal
from services.test_service import TestService


class TestController(BaseController):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self):
        return TestService().get(self.get_request_content())

    def post(self):
        return TestService().post(self.get_request_content())

    def patch(self):
        return TestService().patch(self.get_request_content())


if __name__ == "__main__":
    TestController().test_log()

import json

import requests
from flask import request
from flask_restful import Resource
from flask import make_response
from tools.request_tools import RequestTools
from config import get_user_center_conf, get_env


class BaseController(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request_tools = RequestTools()

    def return_error(self, error_code, error_msg=None, status_code=200):
        self.request_tools.return_error(error_code, error_msg, status_code)

    @staticmethod
    def transfer_to_platform(url, data=None, method="post", headers=None):
        request_body = {} if data is None else data
        request_headers = {} if headers is None else headers
        if "Content-Type" not in request_headers:
            request_headers["Content-Type"] = "application/json"
            request_body = json.dumps(request_body)
        response = requests.request(method, url, data=request_body, headers=request_headers)
        if response.status_code != 200:
            RequestTools().return_error(10019)
        response_json = response.content.decode('utf-8')
        response_dict = json.loads(response_json)
        return response_dict

    @staticmethod
    def formate_args(args, format_str=False, format_keys=True,
                     format_eval=True):
        """
        参数格式化
        :param args: 参数字典
        :param format_str: 是否需要把所有int类型,强转成字符串
        :param format_eval: 是否开启 把字符串 '["a","b"]' '{"a":1,"b":"1"}' 强转回list dict
        :param format_keys: 是否开启 把key的值 转为全小写
        :return:
        """
        tmp = {}
        for key, value in args.items():
            if format_eval and isinstance(value, str) and value:
                if value[0] in ("[", "{", "(") and value[-1] in ("]", "}", ")"):
                    value = eval(value)
            if format_keys:
                key_lower = key.lower()
            else:
                key_lower = key
            if format_str:
                if isinstance(value, (int, float)):
                    value = str(value)
            tmp[key_lower] = value
        formated_args = dict(filter(lambda x: x[1] != '', tmp.items()))
        return formated_args

    def get_argument_dict(self, must_keys=None, format_str=False, format_keys=True, format_eval=True, check_form_token=False, time_key_list=None):
        """
        :param must_keys: must_keys=["aa", "bb"] 判断出入列表里的值,是否在请求参数里,没有报错
        :param format_str: 是否需要把所有int类型,强转成字符串
        :param format_eval: 是否开启 把字符串 '["a","b"]' '{"a":1,"b":"1"}' 强转回list dict
        :param format_keys: 是否开启 把key的值 转为全小写
        :param check_form_token: 是否校验表单中的随机字符串，所有会修改数据的请求，都应该校验！！
        :param time_key_list: 转换时区的校验时间key补充字段列表
        :return:
        """
        # 获取参数字典
        request_args = self.get_request_content()

        request_args = self.formate_args(request_args, format_str, format_keys, format_eval)

        if get_env() != 'dev' and check_form_token:
            if 'form_token' not in request_args:
                self.return_error(10018)
            check_url = get_user_center_conf()[get_env()]['base_url'] + '/transfer/' + str(request_args['form_token'])
            check_result = self.transfer_to_platform(check_url)
            if not check_result:
                self.return_error(10018)
            request_args.pop('form_token')

        # 判断必填字段
        if must_keys:
            for key in must_keys:
                if key not in request_args:
                    self.return_error(20003)
        return self.timezone_transform(request_args, time_key_list)

    def get_request_content(self):
        """
        获取请求参数,如果参数中有data字段,直接返回data字段内容
        :return:
        """
        request_type = request.headers.get('Content-Type')
        if request_type:
            content_type = request_type.split(';')[0].lower()
            if content_type == "application/json":
                request_args = request.get_json()
            else:  # multipart/form-data
                request_args = request.form
                request_args = request_args.to_dict()
        else:
            request_args = {}
            for i in request.values.dicts:
                for k, v in i.items():
                    request_args[k] = v

        return request_args

    def make_html_response(self, value):
        resp = make_response(value)
        resp.headers['Content-Type'] = 'text/html'
        return resp

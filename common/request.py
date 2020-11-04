import requests, os, logging
from common.opmysql import OperationDbInterface
from public import config
from pymysql import escape_string
import json

class RequestInterface(object):

    #定义处理不同类型的请求参数，包含字典，字符串，空值
    def __new_param(self, param):
        try:
            if isinstance(param, str) and param.startswith('{'):
                new_param = eval(param)
            elif param == None:
                new_param = ''
            else:
                new_param = param
        except Exception as error:
            new_param = ''
            logging.basicConfig(file_name = config.src_path + '/log/syserror.log',
                                 level = logging.DEBUG,
                                 format = '%(actime)s %(file_name)s [line:%(lineno)d] %(levelname)s %(messqge)s')
            logger = logging.getLogger(__name__)
            logger.exception(error)
        return new_param


    #post请求，参数在body中
    def __http_post(self,interface_url, headersdata, interface_params):
        try:
            if interface_url :
                temp_interface_param = self.__new_param(interface_params)
                response = requests.post(url=interface_url, headers=headersdata, data=temp_interface_param,
                                        verify=False, timeout=10)
                if response.status_code == 200:
                    result = {'code': '0', 'message': 'success', 'data': response.text}
                else:
                    result = {'code': '1', 'message': 'response status is return fail', 'data': []}
            else:
                result = {'code': '2', 'message': 'interface url is null', 'data': []}
        except Exception as error:
            result = {'code': '500', 'message': 'server error', 'data': []}
            logging.basicConfig(filename=config.scr_path + '/log/syserror.log',
                                level=logging.DEBUG,
                                format = '%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s')

            logger = logging.getLogger(__name__)
            logger.exception(error)
        return result
    #get请求，参数在接口地址后面
    def __http_get(self, interface_url, headersdata, interface_params):
        try:
            if interface_url:
                temp_interface_param = self.__new_param(interface_params)
                if interface_url.endswith('?'):
                    requrl = interface_url + temp_interface_param
                else:
                    requrl = interface_url + '?' + temp_interface_param
                response = requests.get(url=requrl, headers=headersdata, verify=False, timeout=10)
                #print response
                if response.status_code == 200:
                    result = {'code': '0', 'message': 'success', 'data': response.text}
                    print(result)
                else:
                    result = {'code': '1', 'message': 'response status is return fail', 'data': []}
            else:
                result = {'code': '2', 'message': 'interface url is null', 'data': []}
        except Exception as error:
            result = {'code': '4', 'message': 'server error', 'data': []}
            logging.basicConfig(filename=config.scr_path + '/log/syserror.log',
                               level=logging.DEBUG,
                               format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s')

            logger = logging.getLogger(__name__)
            logger.exception(error)
        return result
    #统一处理http请求
    def http_request(self,interface_url, headersdata, interface_param, request_type):
        try:
            if request_type == 'get' or request_type == 'GET':
                result = self.__http_get(interface_url, headersdata, interface_param)
            elif request_type == 'post' or request_type == 'POST':
                result = self.__http_post(interface_url, headersdata, interface_param)
            else:
                result = {'code': '1', 'message': 'others request type ', 'data': request_type}

        except Exception as error:
            result = {'code': '500', 'message': 'server error', 'data': []}
            logging.basicConfig(filename=config.scr_path + '/log/syserror.log',
                                level=logging.DEBUG,
                                format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s')

            logger = logging.getLogger(__name__)
            logger.exception(error)
        return result

if __name__ == '__main__':
    test_interface = RequestInterface()
    test_db = OperationDbInterface(host_db='localhost', user_db='root', passwd_db='12345678',
                                   name_db='test_interface', port_db=3306, link_type=0)
    sen_sql = "select * from case_interface where id =3"
    params = test_db.select_one(sen_sql)
    if params['code'] == '0000':
        url_interface = params['data']['interface_url']
        headersdata = params['data']['headersdata']
        interface_params = params['data']['interface_params']
        request_type = params['data']['exe_mode']
        if url_interface != '' and headersdata != '' and interface_params != '' and request_type != '':
            result = test_interface.http_request(interface_url=url_interface, headersdata=headersdata,
                                                  interface_param=interface_params, request_type=request_type)
            if result['code'] == '0':
                result_resp = result['data']
                print(type(result_resp))
                print(json.loads(result_resp))
                print("update case_interface set result_interface='{}' where id=3".format(escape_string(result_resp)))
                test_db.op_sql("update case_interface set result_interface='{}' where id=3".format(escape_string(result_resp)))
            else:
                print("deal with the result fail")
        else:
            print("testcase is null")
    else:
        print("get the url case data  fail")



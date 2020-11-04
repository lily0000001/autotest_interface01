import os,logging,json
from common import opmysql
from public import config
operation_db = opmysql.OperationDbInterface()
#封装接口返回值校验
class CompareParam(object):

    def __init__(self, interface_params):
        self.interface_params = interface_params
        self.id_case = interface_params['id']
        self.result_list_response = []
        self.params_to_compare = interface_params['params_to_compare']

    # 定义关键字值参数比较
    def compare_code(self, result_interface):
        try:
            if result_interface.startswith('{') and isinstance(result_interface, str):
                temp_result_interface = json.loads(result_interface)
                temp_code_to_compare = self.interface_params['code_to_compare']
                if temp_code_to_compare in temp_result_interface.keys():
                    if str(temp_result_interface[temp_code_to_compare]) == self.interface_params['code_expect']:
                        result = {'code': '0', 'message': 'pass', 'data': []}
                        operation_db.op_sql("update case_interface set code_actual= '%s',result_code_compare= %s where "
                                            "id=%s" % (temp_result_interface[temp_code_to_compare], 1, self.id_case))

                    elif str(temp_result_interface[temp_code_to_compare]) != str(self.interface_params['code_expect']):
                        result = {'code': '1', 'message': 'fail', 'data': []}
                        operation_db.op_sql("update case_interface set code_actual= '%s',result_code_compare= %s where "
                                            "id= %s " % (temp_result_interface[temp_code_to_compare], 0, self.id_case))
                    else:
                        result = {'code': '2', 'message': '比较关键字错误', 'data': []}
                        operation_db.op_sql("update case_interface set code_actual='%s', result_code_compare= %s where "
                                            "id=%s" % (temp_result_interface[temp_code_to_compare], 3, self.id_case))
                else:
                    result = {'code': '3', 'message': 'no keyvalue', 'data': []}
                    operation_db.op_sql("update case_interface set result_code_compare=%s where id=%s"
                                        % (2, self.id_case))
            else:
                result = {'code': '4', 'message': '返回包错误', 'data': []}
                operation_db.op_sql("update case_interface set result_code_compare=%s where id=%s" % (4, self.id_case))
        except Exception as error:
            result = {'code': '5', 'message': '关键字参数比较异常', 'data': []}
            operation_db.op_sql(" update case_interface set result_code_compare=%s where id = %s " % (9, self.id_case))
            logging.basicConfig(filename=config.src_path + '/log/syserror.log',
                                level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(error)
        finally:
            return result

    #定义接口返回数据中的参数写入列表
    def get_compare_params(self,result_interface):
        try:
            if result_interface.startswith('{') and isinstance(result_interface, str):
                temp_result_interface = json.loads(result_interface)
                self.result_list_response = temp_result_interface.keys()
                result = {'code': '0', 'message': 'success', 'data': self.result_list_response}
            else:
                result = {'code': '1', 'message': '返回数据包不合法', 'data': []}
        except Exception as error:
            result = {'code': '2', 'message': '处理数据异常', 'data': []}
            logging.basicConfig(filename=config.src_path + '/log/syserror.log',
                                level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(error)
        finally:
            return result

    #定义递归方法
    def __recur_params(self, result_interface):
      #定义递归操作，将接口返回数据中的参数名写入列表中（去重）
        try:
            if result_interface.startswith('{') and isinstance(result_interface, str):
                temp_result_interface = json.loads(result_interface)
                self.__recur_params(temp_result_interface)
            elif isinstance(result_interface, dict):
                for param, value in result_interface.items():
                    self.result_list_response.append(param)
                    if isinstance(value, list):
                        for param in value:
                            self.__recur_params(param)
                    elif isinstance(value, dict):
                        self.__recur_params(value)
                    else:
                        continue
            else:
                pass
        except Exception as error:
            logging.basicConfig(filename=config.src_path + '/log/syserror.log',
                                level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(error)
            result = {'code': '9999', 'message': '数据处理异常', 'data': []}

    #定义参数完整性比较方法，将传参值与__recur_params方法返回结果进行比较
    def compare_params_comlpete(self,result_interface):
        try:
           temp_compare_params = self.__recur_params(result_interface)
           if temp_compare_params['code'] == '0000':
               temp_result_list_response = temp_compare_params['data']
               if self.params_to_compare.startwith('[') and isinstance (self.params_to_compare,str):
                   list_params_to_compare = eval(self.params_to_compare)
                   if set(list_params_to_compare).issubset(set(temp_result_list_response)):
                       result = {'code':'0','message':'参数完整性一致','data':[]}
                       operation_db.op_sql('update case_interface set params_actual= "%s",result_params_compare=%s,'
                                           'where id="%s"'%(temp_result_list_response,1,self.id_case))
                   else:
                       result = {'code':'3001','message':'实际结果中元素不都在预期结果中','data':[]}
                       operation_db.op_sql('update case_interface set params_actual= "%s",result_params_compare=%s,'
                                           'where id="%s"' %(temp_result_list_response,0,self.id_case))
               else:
                   result = {'code':'4001','message':'用例中待比较的参数集错误','data':self.params_to_compare }
           else:
                result = {'code': '2001', 'message':'error','data':[] }
                operation_db.op_sql('update case_interface set result_params_compare=%s where id = "%s"' %(2,self.id_case))
        except Exception as error:
            result = {'code':'9999','messqge':'参数完整性比较异常','data':[]}
            operation_db.op_sql('update case_interface set result_params_compare=%s where id = "%s"' % (9, self.id_case))
            logging.basicConfig(filename=config.src_path + '/log/syserror.log',
                                level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(error)
        finally:
            return result
if __name__ == "__main__":
    sen_sql = "select * from case_interface where  id = 4"
    params_interface = operation_db.select_one(sen_sql)
    result_interface = params_interface['data']['result_interface']
    print(result_interface)
    # 实例
    test_compare_param = CompareParam(params_interface['data'])
    #关键字参数值比较
    result_compare_code = test_compare_param.compare_code(result_interface)
    print(result_compare_code)
    #参数完整性比较
    result_compare_params_complete = test_compare_param.compare_params_comlpete(result_interface)
    print(result_compare_params_complete)


    




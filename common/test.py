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
                        operation_db.op_sql("update case_interface set code_actual= '%s',result_code_compare=%s where "
                                            "id=%s" % (temp_result_interface[temp_code_to_compare], 1, self.id_case))

                    elif str(temp_result_interface[temp_code_to_compare]) != str(self.interface_params['code_except']):
                        result = {'code': '1', 'message': 'fail', 'data': []}
                        operation_db.op_sql("update case_interface set code_actual=%s,result_code_compare=%s where id=%s"
                                          % (temp_result_interface[temp_code_to_compare], 0, self.id_case))
                    else:
                        result = {'code':'2','message':'compare keyvalue error','data':[]}
                        operation_db.op_sql("update case_interface set code_actual=%s,result_code_compare=%s where id=%s"
                                          % (temp_result_interface[temp_code_to_compare], 3, self.id_case))
                else:
                    result = {'code':'3','message':'no keyvalue','data':[]}
                    operation_db.op_sql("updated case_interface set result_code_compare=%s where id=%s" %(2,self.id_case))
            else:
                result = {'code':'4','message':'reponse package error','data':[]}
                operation_db.op_sql("updated case_interface set result_code_compare=%s where id=%s" %(4,self.id_case))
        except Exception as error:
            result = {'code': '5', 'message': '关键字参数比较异常', 'data': []}
            operation_db.op_sql(" update case_interface set result_code_compare=%s where id = %s " % (9, self.id_case))
            logging.basicConfig(filename=config.src_path + '/log/syserror.log',
                                level= logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(error)
        finally:
            return result

if __name__ == "__main__":
    sen_sql = "select * from case_interface where name_interface = '获取手机号信息' and id = 1"
    params_interface = operation_db.select_one(sen_sql)
    result_interface = params_interface['data']['result_interface']
    print(result_interface)
    # 实例
    test_compare_param = CompareParam(params_interface['data'])
    #关键字参数值比较
    result_compare_code = test_compare_param.compare_code(result_interface)
    print(result_compare_code)





import logging, os, pymysql
from public import config
class OperationDbInterface(object):
    #定义初始化数据库连接
    def __init__(self, host_db='localhost', user_db='root', passwd_db='12345678'
                 , name_db='test_interface', port_db=3306, link_type=0):
        try:
            if link_type == 0:
                #创建数据库连接，返回字典

                self.conn = pymysql.connect(host=host_db, user=user_db, passwd=passwd_db,
                                            db=name_db, port=port_db, charset='utf8',
                                            cursorclass=pymysql.cursors.DictCursor)
            else:
                #创建数据库连接，返回元组
                self.conn = pymysql.connect(host=host_db, user=user_db, passwd=passwd_db,
                                    db =name_db, port=port_db, charset='utf8')
            self.cur = self.conn.cursor()
        except pymysql.Error as e:
            print("创建数据库失败mysql error %d: %s" % (e.args[0], e.args[1]))
            logging.basicConfig(filename=config.src_path +'/log/syserror.log',level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)

            logger.exception(e)
        #定义单条数据操作，增加，删除，修改
    def op_sql(self,condition):
        try:
            self.cur.execute(condition)
            self.conn.commit()
            result = {'code': '0000', 'message': '执行通用操作成功', 'data': []}
        except pymysql.Error as e:
            self.conn.rollback()
            result = {'code': '9999', 'message': '执行通用操作异常', 'data': []}
            print("数据库错误|op_sql %d:%s" % (e.args[0], e.args[1]))
            logging.basicConfig(filename=config.src_path + '/log/syserror.log', level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)

            logger.exception(e)
        return result
    #查询表中单条数据
    def select_one (self,condition):
        try:
            rows_affect = self.cur.execute(condition)
            if rows_affect > 0:
                #获取一条结果
                results = self.cur.fetchone()
                result = {'code': '0000', 'message': '执行单条查询成功', 'data': results}
                print(result)
            else:
                result = {'code': '0000', 'message': '执行单条查询成功', 'data': []}
        except pymysql.Error as e:
            self.conn.rollback()
            result = {'code': '9999', 'message': '执行通用操作异常', 'data': []}
            print("数据库错误|select_one %d:%s" % (e.args[0], e.args[1]))
            logging.basicConfig(filename=config.src_path + '/log/syserror.log', level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)

            logger.exception(e)
        return result
    # select many results
    def select_all (self,condition):
        try:
            rows_affect = self.cur.execute(condition)
            if rows_affect > 0:
                self.cur.scoll(0, mode='absolute')
                results = self.cur.fetchall()
                result = {'code': '0000', 'message': '执行单条查询成功', 'data': results}
            else:
                result = {'code': '0000', 'message': '执行单条查询成功', 'data': []}
        except pymysql.Error as e:
            self.conn.rollback()
            result = {'code':'9999','message': '', 'data': []}
            print("数据库错误|select_all %d:%s" % (e.args[0], e.args[1]))
            logging.basicConfig(filename=config.src_path + '/log/syserror.log', level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)

            logger.exception(e)
        return result
    #定义表中插入多条数据
    def insert_more(self,condition,params):
        try:
            results = self.cur.executemany(condition, params)
            self.conn.commit()
            result = {'code': '0000', 'message': '执行批量查询成功', 'data': int(results)}
        except pymysql.Error as e:
            self.conn.rollback()
            result = {'code': '9999', 'message': '执行通用操作异常', 'data': []}
            print("数据库错误|op_sql %d:%s" % (e.args[0], e.args[1]))
            logging.basicConfig(filename=config.src_path + '/log/syserror.log', level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)

            logger.exception(e)
        return result
    #关闭数据库
    def __del__(self):
        if self.cur != None:
            self.cur.close()
        if self.conn != None:
            self.conn.close()
if __name__ == "__main__":
    test = OperationDbInterface()
    result_select_one = test.select_one("select * from case_interface")
    if result_select_one['code'] == '0000':
        print(result_select_one['data'])
    else:
        print(result_select_one['message'])



















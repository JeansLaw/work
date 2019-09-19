import json
import os

import pymysql


class sqlUtil(object):
    __conn = None   #数据库连接器
    __filepath = None   #数据库配置文件路径

    # 设置数据库配置文件路径
    def settingPath(self, path=None):
        if os.path.exists(path):
            self.__filepath = path
        else:
            print("配置文件不存在")

    # 创建数据库连接
    def __connect(self):
        if self.__filepath == None:
            getcwd = os.path.abspath(os.path.dirname(os.getcwd()))
            self.__filepath = os.path.join(getcwd + r"\setting", "dbSetting.json")
            # print(self.__filepath)

        with open(self.__filepath, "r") as f:
            load_dict = json.load(f)
            conn = pymysql.connect(
                host=load_dict["connection"]["host"],
                port=load_dict["connection"]["port"],
                user=load_dict["connection"]["user"],
                password=load_dict["connection"]["password"],
                db=load_dict["connection"]["db"],
                charset=load_dict["connection"]["charset"]
            )
            self.__conn = conn
            # print(conn)
            return self.__conn

    def __disConnect(self):
        self.__conn.close()

    # 查询操作,返回结果
    def query(self, sql):
        """
        :param sql: SELECT * FROM table
        :return: 返回查询结果
        """

        try:
            conn = self.__connect()
            cursor = conn.cursor()
            cursor.execute(sql)
            queryResult = cursor.fetchall()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            self.__disConnect()
            return queryResult

    # 插入、更新、删除
    def excute(self, sql):
        """
        :param sql: INSERT or UPDATE or DELETE
        """
        conn = self.__connect()
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            conn.commit()
        except Exception as e:
            print(e)
            conn.rollback()
        finally:
            cursor.close()
            self.__disConnect()

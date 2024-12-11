from django.db import connection
from django.db.utils import OperationalError


class SQLManager:

    @staticmethod
    def fetchmany(query, params=None):
        """
        执行查询并返回所有结果
        :param query: SQL 查询语句
        :param params: 查询参数
        :return: 查询结果
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, params or [])
                result = cursor.fetchall()  # 获取所有查询结果
            return result
        except OperationalError as e:
            print(f"Error executing query: {e}")
            return None

    @staticmethod
    def fetchone(query, params=None):
        """
        执行查询并返回单条记录
        :param query: SQL 查询语句
        :param params: 查询参数
        :return: 查询结果
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, params or [])
                result = cursor.fetchone()  # 获取单条查询结果
            return result
        except OperationalError as e:
            print(f"Error executing query: {e}")
            return None

    @staticmethod
    def execute_update(query, params=None):
        """
        执行更新、删除等操作并返回受影响的行数
        :param query: SQL 更新/删除语句
        :param params: 更新参数
        :return: 受影响的行数
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, params or [])
                rows_affected = cursor.rowcount  # 获取影响的行数
            return rows_affected
        except OperationalError as e:
            print(f"Error executing update: {e}")
            return 0

    @staticmethod
    def execute(query, params=None):
        """
        执行插入操作并返回插入的主键
        :param query: SQL 插入语句
        :param params: 插入参数
        :return: 插入的主键
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, params or [])
                return cursor.lastrowid  # 获取插入记录的主键
        except OperationalError as e:
            print(f"Error executing insert: {e}")
            return None

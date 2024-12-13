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

    @staticmethod
    def fetchmany_total(query, params=None):
        """
        执行带有 SQL_CALC_FOUND_ROWS 的查询，并返回结果和总行数
        :param query: SQL 查询语句（包含 SQL_CALC_FOUND_ROWS）
        :param params: 查询参数
        :return: 查询结果和总行数 (result, total_count)
        """
        try:
            with connection.cursor() as cursor:
                # 执行主查询
                cursor.execute(query, params or [])
                result = cursor.fetchall()  # 获取查询结果

                # 查询匹配的总行数
                cursor.execute("SELECT FOUND_ROWS()")
                total_count = cursor.fetchone()[0]  # 获取总行数
            return result, total_count
        except OperationalError as e:
            print(f"Error executing query with SQL_CALC_FOUND_ROWS: {e}")
            return None, 0

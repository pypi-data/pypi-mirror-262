import re

import emoji
import pymysql


# 喵喵自己的SQL
class MySql:
    cursor = None

    # 数据库连接
    def __init__(self, con: dict):
        self._config = con
        self._sjk = pymysql.connect(**self._config)
        self.cursor = self._sjk.cursor()

    # 数据库断开
    def __del__(self):
        self._sjk.commit()
        self.cursor.close()
        self._sjk.close()

    # 获取某表的数据条数
    def get_len(self, table: str):
        qur = f"select * from `{table}`;"
        res = self.cursor.execute(qur)
        return res

    # 判断某数据是否在表中
    def if_in_it(self, table: str, cols: list, vals: list) -> bool:
        qur = f"SELECT * FROM `{table}` WHERE {' AND '.join([col + ' = ' + self.format_val(val) for col, val in zip(cols, vals)])} "
        print(qur)
        res = self.cursor.execute(qur)

        if res == 0:
            return False
        else:
            return True

    def sel(self, table: str, condition: str = None, out_cols: list = None, order: str = None):
        qur = f"SELECT {'*' if not out_cols else ', '.join('`' + out_col + '`' for out_col in out_cols)} FROM `{table}` " \
              f"WHERE {condition if condition else 1} " \
              f"{'' if not order else 'ORDER BY `' + order + '`'}"
        print(qur)
        res = self.cursor.execute(qur)
        return res

    def sel_eq(self, table: str, cols: list[str], vals: list[str], out_cols: list = None, order: str = None,
               use_or: bool = False):
        qur = f"SELECT {'*' if not out_cols else ', '.join('`' + out_col + '`' for out_col in out_cols)} FROM `{table}` " \
              f"WHERE {(' OR ' if use_or else ' AND ').join([col + ' = ' + self.format_val(val) for col, val in zip(cols, vals)])} " \
              f"{'' if not order else 'ORDER BY `' + order + '`'}"
        print(qur)
        res = self.cursor.execute(qur)
        return res

    def sel_like(self, table: str, cols: list[str], vals: list[str], out_cols: list = None, order: str = None,
                 use_or: bool = False):
        qur = f"SELECT {'*' if not out_cols else ', '.join('`' + out_col + '`' for out_col in out_cols)} FROM `{table}` " \
              f"WHERE {(' OR ' if use_or else ' AND ').join([col + ' LIKE ' + self.format_val(val) for col, val in zip(cols, vals)])} " \
              f"{'' if not order else 'ORDER BY `' + order + '`'}"
        print(qur)
        res = self.cursor.execute(qur)
        return res
        pass

    def add(self, table: str, cols: list[str], vals: list[str]):
        qur = f"INSERT INTO `{table}` ({', '.join([col for col in cols])}) VALUES " \
              f"({', '.join([self.format_val(val) for val in vals])});"
        print(qur)
        res = self.cursor.execute(qur)
        return res

    def delete(self, table: str, cols: list[str], vals: list, use_or: bool = False):
        qur = f"DELETE FROM `{table}` " \
              f"WHERE {(' OR ' if use_or else ' AND ').join([col + '=' + self.format_val(val) for col, val in zip(cols, vals)])};"
        print(qur)
        res = self.cursor.execute(qur)
        return res

    def update(self, table: str, new_cols: list[str], new_vals: list[str], old_cols: list[str], old_vals: list[str],
               use_or: bool = False):
        qur = f"UPDATE `{table}` " \
              f"SET {', '.join([col + ' = ' + self.format_val(val) for col, val in zip(new_cols, new_vals)])} " \
              f"WHERE {(' OR ' if use_or else ' AND ').join([col + '=' + self.format_val(val) for col, val in zip(old_cols, old_vals)])};"
        print(qur)
        res = self.cursor.execute(qur)
        return res

    def format_val(self, s):
        if type(s) == str:
            s = emoji.demojize(s, delimiters=(" ", " "))
            s = s.replace(r'\"', '"').replace("\\",'').replace('"', r'\"')
            return '"' + s + '"'
        else:
            return str(s)



# OpenMySql的with版本
class OpenMySql:
    sql = None

    def __init__(self, con: dict):
        self.sql = MySql(con)

    def __enter__(self):
        return self.sql

    def __exit__(self, exc_type, exc_val, exc_tb):
        del self.sql

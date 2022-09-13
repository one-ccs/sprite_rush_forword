#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import sqlite3


def construct_response(status, msg):
    return json.dump({'status': status, 'msg': msg})


class UserDB:
    def __init__(self, db_path) -> None:
        self.db_path = db_path

    def __del__(self) -> None:
        pass

    def query():
        pass
    
    def insert(id, uname, pwd, score):
        result = {'state': True, 'msg': ''}
        # 连接数据库，没有则自动创建
        connection = sqlite3.connect('./db/user.db')
        # 获取游标
        cursor = connection.cursor()
        try:
            # 执行 SQL 语句
            cursor.execute(f'insert into user(uname, pwd, score) values("{uname}", "{pwd}", {score})')
        except sqlite3.IntegrityError as e:
            result['state'] = False
            result['msg'] ='用户名已存在，请修改后重试！'
        # 关闭游标
        cursor.close()
        # 提交事务
        connection.commit()
        # 关闭数据库连接
        connection.close()

        return result

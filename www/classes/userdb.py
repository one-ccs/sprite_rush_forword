#!/usr/bin/env python
# -*- coding: utf-8 -*-
from werkzeug.security import generate_password_hash, check_password_hash
from os import path
import sqlite3
from classes.user import User


class UserDB:
    def __new__(cls, *arg, **kw):
        # 实现单例模式
        if not hasattr(cls, '_instance'):
            cls._instance = super(UserDB, cls).__new__(cls)
        return cls._instance

    def __init__(self, db_path):
        if not path.isfile(db_path):
            raise ValueError(f'无效的数据库文件路径({db_path}).')
        self.db_path = db_path

    def __type_check(self, user):
        if not isinstance(user, User):
            raise TypeError(f'类型错误: 期待 {type(User)} 类型, 却传入{type(user)} 类型.')

    def query_by_uname(self, user):
        self.__type_check(user)

    def query_all(self):
        pass

    def check_pwd(self, user):
        """ 校验密码 """
        result = {'state': True, 'msg': '', 'pwd': ''}
        connection = sqlite3.connect(self.db_path)
        try:
            connection.execute(f'select pwd from user where uname="{user.uname}"')
            pwd = connection.fetchone()
        except sqlite3.IntegrityError as e:
            result['state'] = False
            result['msg'] = f'未查找到用户: "{user.uname}".'

        connection.close()

        return result
    
    def regist(self, user):
        """ 用户注册 """
        result = {'state': True, 'msg': ''}
        # 加密密码
        pwd = generate_password_hash(user.pwd)[14:]
        # 连接数据库，没有则自动创建
        connection = sqlite3.connect(self.db_path)
        try:
            # 执行 SQL 语句
            connection.execute(f'insert into user(uname, pwd, score) values("{user.uname}", "{pwd}", {user.score})')
        except sqlite3.IntegrityError as e:
            result['state'] = False
            result['msg'] = '用户名已存在，请修改后重试！'
        finally:
            # 提交事务
            connection.commit()
            # 关闭数据库连接
            connection.close()

        return result

    def logoff(self, user):
        """ 用户注销 """
        result = {'state': True, 'msg': ''}
        # 加密密码
        pwd = generate_password_hash(user.pwd)[14:]
        # 连接数据库，没有则自动创建
        connection = sqlite3.connect(self.db_path)
        try:
            # 执行 SQL 语句
            connection.execute(f'insert into user(uname, pwd, score) values("{user.uname}", "{pwd}", {user.score})')
        except sqlite3.IntegrityError as e:
            result['state'] = False
            result['msg'] = '用户名已存在，请修改后重试！'
        finally:
            # 提交事务
            connection.commit()
            # 关闭数据库连接
            connection.close()

        return result

    def modify(self, user):
        """ 用户修改 """
        pass

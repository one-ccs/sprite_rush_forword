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

    def query_by_uname(self, user):
        pass

    def query_all(self):
        pass

    def check_pwd(self, user):
        """ 校验密码 """
        if not isinstance(user, User):
            raise TypeError(f'类型错误: 期待 {type(User)} 类型, 却传入{type(user)} 类型.')
        result = {'state': True, 'msg': '', 'pwd': ''}

        connection = sqlite3.connect(self.db_path)
        try:
            t = (user.name, )
            connection.execute('SELECT pwd from user where uname=?', t)
            pwd = connection.fetchone()
        except sqlite3.IntegrityError as e:
            result['state'] = False
            result['msg'] = f'未查找到用户: "{user.uname}".'

        connection.close()

        return result
    
    def regist(self, user):
        """ 用户注册 """
        if not isinstance(user, User):
            raise TypeError(f'类型错误: 期待 {type(User)} 类型, 却传入{type(user)} 类型.')
        result = {'state': True, 'msg': ''}

        pwd = generate_password_hash(user.pwd)[21:]

        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        try:
            t = (user.uname, pwd, user.score)
            cursor.execute('INSERT INTO user(uname, pwd, score) VALUES(?, ?, ?)', t)
        except sqlite3.IntegrityError as e:
            result['state'] = False
            result['msg'] = '用户名已存在，请修改后重试！'
        finally:
            connection.close()

        return result

    def logoff(self, user):
        """ 用户注销 """
        if not isinstance(user, User):
            raise TypeError(f'类型错误: 期待 {type(User)} 类型, 却传入{type(user)} 类型.')
        result = {'state': True, 'msg': ''}


        return result

    def modify(self, user):
        """ 用户修改 """
        if not isinstance(user, User):
            raise TypeError(f'类型错误: 期待 {type(User)} 类型, 却传入{type(user)} 类型.')
        result = {'state': True, 'msg': ''}

        # 加密密码
        pwd = generate_password_hash(user.pwd)[21:]
        # 连接数据库，没有则自动创建
        connection = sqlite3.connect(self.db_path)
        # 获取游标
        cursor = connection.cursor()
        try:
            t = (user.uname, pwd, user.id)
            # 执行 SQL 语句
            cursor.execute('UPDATE user SET uname=?,pwd=? WHERE id=?', t)
        except sqlite3.IntegrityError as e:
            result['state'] = False
            result['msg'] = '用户名已存在，请修改后重试！'
        finally:
            if cursor.rowcount == 0:
                result['state'] = False
                result['msg'] = '未找到该用户!'
            # 关闭游标
            cursor.close()
            # 提交事务
            connection.commit()
            # 关闭数据库连接
            connection.close()

        return result

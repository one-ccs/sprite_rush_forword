#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tabnanny import check
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

    def query_by_user(self, user):
        pass

    def query_all(self):
        pass

    def regist(self, user):
        """ 用户注册 """
        if not isinstance(user, User):
            raise TypeError(f'类型错误: 期待 {type(User)} 类型, 却传入{type(user)} 类型.')
        result = None
        # result = {'state': True, 'msg': ''}

        pwd = generate_password_hash(user.pwd)[21:]

        connection = sqlite3.connect(self.db_path)
        rowcount = 0
        try:
            t = (user.user, pwd, user.score)
            with connection:
                rowcount = connection.execute('INSERT INTO user(user, pwd, score) VALUES(?, ?, ?)', t).rowcount
        except sqlite3.IntegrityError as e:
            result = None
            # result['state'] = False
            # result['msg'] = '用户名已存在，请修改后重试'
        finally:
            if(not rowcount or rowcount == 0):
                result = None
                # result['state'] = False
                # result['msg'] = '用户名已存在，请修改后重试'
            else:
                result = True
            connection.close()

        return result

    def login(self, user):
        """ 校验密码, 并返回 User """
        if not isinstance(user, User):
            raise TypeError(f'类型错误: 期待 {type(User)} 类型, 却传入{type(user)} 类型.')
        result = None

        connection = sqlite3.connect(self.db_path)
        # 查询密码
        row = ()
        try:
            t = (user.user, )
            row = connection.execute('SELECT id,pwd,score from user where user=?', t).fetchone()
        finally:
            if row:
                # 查询成功
                if not check_password_hash(f'pbkdf2:sha256:260000${row[1]}', user.pwd):
                    user.pwd = 'None'
                    result = user
                else:
                    result = User(user.user, row[1], row[2])
                    result.id = row[0]
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
        try:
            t = (user.user, pwd, user.id)
            # 执行 SQL 语句, 使用 with 语句块将自动 commit 或 rollback
            with connection:
                rowcount = connection.execute('UPDATE user SET user=?,pwd=? WHERE id=?', t).rowcount
        except sqlite3.IntegrityError as e:
            result['state'] = False
            result['msg'] = '用户名已存在，请修改后重试'
        finally:
            if rowcount == 0:
                result['state'] = False
                result['msg'] = '未找到该用户'
            else:
                result['state'] = True
                result['msg'] = '修改成功'
            # 必须手动关闭数据库连接
            connection.close()

        return result

    def modify_score(self, user):
        """ 分数修改 """
        if not isinstance(user, User):
            raise TypeError(f'类型错误: 期待 {type(User)} 类型, 却传入{type(user)} 类型.')
        result = {'state': True, 'msg': ''}
        
        connection = sqlite3.connect(self.db_path)
        try:
            t = (user.score, user.id)
            with connection:
                rowcount = connection.execute('UPDATE user SET score=? WHERE id=?', t).rowcount
        except sqlite3.IntegrityError as e:
            result['state'] = False
            result['msg'] = '404'
        finally:
            if rowcount == 0:
                result['state'] = False
                result['msg'] = '未找到该用户'
            else:
                result['state'] = True
                result['msg'] = '修改成功'
            # 必须手动关闭数据库连接
            connection.close()

        return result

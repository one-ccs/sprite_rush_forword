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

    def query_all_and_user(self, user):
        """ 返回排名前二十和当前用户分数 """
        if not isinstance(user, User):
            raise TypeError(f'类型错误: 期待 {type(User)} 类型, 却传入{type(user)} 类型.')
        all = one = None

        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        try:
            # all = connection.execute('SELECT user,score FROM user ORDER BY score DESC LIMIT 20').fetchall()
            all = connection.execute('''
                SELECT u.user,u.score,(SELECT count(distinct(score))
                    FROM user
                    WHERE score>=u.score
                ) AS rank
                FROM user AS u
                ORDER BY score DESC
                LIMIT 20
            ''').fetchall()
            # one = connection.execute('SELECT score FROM user WHERE user=?', (user.user, )).fetchone()
            one = connection.execute('''
                SELECT user,score,rank
                    FROM (SELECT u.user,u.score,(SELECT count(distinct(score)) FROM user WHERE score>=u.score ) AS rank FROM user AS u ORDER BY score DESC)
                    WHERE user=?
            ''', (user.user, )).fetchone()
        except sqlite3.IntegrityError:
            pass
        finally:
            connection.close()

        return (all, one)

    def regist(self, user):
        """ 用户注册 """
        if not isinstance(user, User):
            raise TypeError(f'类型错误: 期待 {type(User)} 类型, 却传入{type(user)} 类型.')
        result = False

        connection = sqlite3.connect(self.db_path)
        rowcount = 0
        try:
            pwd = generate_password_hash(user.pwd)[21:]
            t = (user.user, pwd, user.score)
            with connection:
                rowcount = connection.execute('INSERT INTO user(user, pwd, score) VALUES(?, ?, ?)', t).rowcount
        except sqlite3.IntegrityError:
            pass
        finally:
            if(rowcount and rowcount > 0):
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
                    user.errmsg = '密码错误'
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

    def modify(self, user, encryption=True):
        """ 用户修改, 默认加密密码 """
        if not isinstance(user, User):
            raise TypeError(f'类型错误: 期待 {type(User)} 类型, 却传入{type(user)} 类型.')
        result = user

        # 加密密码
        if encryption:
            pwd = generate_password_hash(user.pwd)[21:]
        else:
            pwd = user.pwd
        # 连接数据库，没有则自动创建
        connection = sqlite3.connect(self.db_path)
        rowcount, row, err_exist = 0, None, False
        try:
            t = (user.user, pwd, user.id)
            # 执行 SQL 语句, 使用 with 语句块将自动 commit 或 rollback
            with connection:
                rowcount = connection.execute('UPDATE user SET user=?,pwd=? WHERE id=?', t).rowcount
            t = (user.user, )
            row = connection.execute('SELECT id,pwd,score from user where user=?', t).fetchone()
        except sqlite3.IntegrityError:
            err_exist = True
            user.errmsg = '用户名已存在, 请勿重复'
        finally:
            if rowcount == 0 and not err_exist and not row:
                user.errmsg = '未找到该用户'
            else:
                # 修改成功
                user.id, user.pwd, user.score = row[0], row[1], row[2]
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

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import request, jsonify
from classes.userdb import UserDB
from classes.user import User
from views import user_blue


userdb = UserDB('./db/user.db')


@user_blue.route('/user/login', methods=['POST'])
def login():
    # 获取表单数据
    uname = request.form.get('uname')
    pwd = request.form.get('pwd')

    # 查询用户

    # 匹配密码

@user_blue.route('/user/regist', methods=['POST'])
def regist():
    # 获取表单数据
    uname = request.form.get('uname')
    pwd = request.form.get('pwd')

    # 插入数据库
    result = userdb.user_blueend(User(uname, pwd))
    if result['state']:
        return jsonify({'status': 200, 'msg': '注册成功'})
    else:
        return jsonify({'status': 304, 'msg': f'注册失败, {result["msg"]}'})
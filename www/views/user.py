#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import request, session, jsonify, make_response
from classes.userdb import UserDB
from classes.user import User
from views import user_blue


userdb = UserDB('./db/user.db')


@user_blue.route('/login', methods=['POST'])
def login():
    # 获取表单数据
    uname = request.form.get('uname')
    pwd = request.form.get('pwd')

    # 查询用户并匹配密码
    result = userdb.check_pwd(User(uname, pwd))
    if result['state']:
        # 校验成功
        result['state'] = 'ok'
        session[uname] = uname
    res = make_response(result)
    res.set_cookie('user', uname)

    return res

@user_blue.route('/regist', methods=['POST'])
def regist():
    # 获取表单数据
    uname = request.form.get('uname')
    pwd = request.form.get('pwd')

    # 插入数据库
    result = userdb.regist(User(uname, pwd))
    if result['state']:
        return jsonify({'state': 'ok', 'msg': '注册成功'})
    else:
        return jsonify({'state': 'fail', 'msg': f'注册失败, {result["msg"]}'})
    # 匹配密码

@user_blue.route('/modify', methods=['POST'])
def modify():
    # 获取表单数据
    uname = request.form.get('uname')
    pwd = request.form.get('pwd')
    cooike_user = request.cookies.get(uname)

    # 判断登陆状态
    if not cooike_user:
        # 未登录
        return jsonify({'state': 'fail', 'msg': '用户未登录'})

    # 修改数据库
    result = userdb.modify(User(uname, pwd))
    if result['state']:
        return jsonify({'state': 'ok', 'msg': '修改成功'})
    else:
        return jsonify({'state': 'fail', 'msg': f'修改失败, {result["msg"]}'})

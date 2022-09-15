#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import request, session, jsonify, make_response
from classes.user import User
from views import user_blue
from app import userdb


@user_blue.route('/session', methods=['POST', 'DELETE'])
def _session():
    res = None
    # 登录
    if request.method == 'POST':
        # 获取表单数据
        user = request.form.get('user')
        pwd = request.form.get('pwd')
        # 查询用户并匹配密码
        result = userdb.login(User(user, pwd))
        # if result['state']:
        if result:
            if result.pwd == 'None':
                # 密码错误
                res = make_response({'state': 'fail', 'msg': '密码错误'}, 403)
            else:
                # 校验成功
                # result['state'] = 'ok'
                session[user] = (result.id, result.pwd)
                # session[user] = (result['id'], result['pwd'])
                session.permanent = True
                res = make_response({'state': 'ok', 'msg': '登录成功'}, 200)
                # res = make_response(result, 200)
                res.set_cookie('user', result.user)
                # res.set_cookie('user', user)
                res.set_cookie('score', str(result.score))
        else:
            # result['state'] = 'fail'
            res = make_response({'state': 'fail', 'msg': '不存在此用户'}, 403)
            # res = make_response(result, 404)

    # 登出
    if request.method == 'DELETE':
        user = request.cookies.get('user')
        if user and user in session:
            session.pop(user)
            res = make_response({'state': 'ok', 'msg': '登出成功'}, 200)
            res.delete_cookie('user')
            res.delete_cookie('score')
        else:
            res = make_response({'state': 'ok', 'msg': '操作失败'}, 405)

    return res

@user_blue.route('/regist', methods=['POST'])
def regist():
    # 获取表单数据
    user = request.form.get('user')
    pwd = request.form.get('pwd')

    # 插入数据库
    result = userdb.regist(User(user, pwd))
    if result['state']:
        return jsonify({'state': 'ok', 'msg': '注册成功'})
    else:
        res = make_response({'state': 'fail', 'msg': f'注册失败, {result["msg"]}'}, 403)
        return res

@user_blue.route('/modify', methods=['POST'])
def modify():
    # 获取表单数据
    user = request.form.get('user')
    pwd = request.form.get('pwd')
    cooike_user = request.cookies.get(user)

    # 判断登陆状态
    if not cooike_user:
        # 未登录
        return jsonify({'state': 'fail', 'msg': '用户未登录'})

    # 修改数据库
    result = userdb.modify(User(user, pwd))
    if result['state']:
        return jsonify({'state': 'ok', 'msg': '修改成功'})
    else:
        return jsonify({'state': 'fail', 'msg': f'修改失败, {result["msg"]}'})

@user_blue.route('/score', methods=['GET', 'POST'])
def score():
    res = None
    user = request.cookies.get('user')

    if request.method == 'GET':
        # 查询
        pass

    if request.method == 'POST':
        # 修改
        score = request.form.get('score')
        if not user or user not in session:
            #未登录
            res = make_response({'state': 'fail', 'msg': '请登录后操作'}, 403)
        else:
            _user = User(user, 'None', score)
            _user.id = session.get(user)[0]
            result = userdb.modify_score(_user)
            if result['state']:
                # 修改成功
                result['state'] = 'ok'
                res = make_response(result, 200)
            else:
                result['state'] = 'fail'
                res = make_response(result, 403)

    return res

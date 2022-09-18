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
        if result:
            if hasattr(result, 'errmsg'):
                # 密码错误
                res = make_response({'state': 'fail', 'msg': '密码错误'}, 403)
            else:
                # 校验成功
                session[user] = {'id': result.id, 'pwd': result.pwd}
                session.permanent = True
                res = make_response({'state': 'ok', 'msg': '登录成功'}, 200)
                res.set_cookie('user', result.user)
                res.set_cookie('score', str(result.score))
        else:
            res = make_response({'state': 'fail', 'msg': '不存在此用户'}, 403)

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
    res = None
    # 获取表单数据
    user = request.form.get('user')
    pwd = request.form.get('pwd')
    # 插入数据库
    result = userdb.regist(User(user, pwd))
    if result:
        res = make_response({'state': 'ok', 'msg': '注册成功'}, 200)
    else:
        res = make_response({'state': 'fail', 'msg': '注册失败, 用户名已存在, 请修改后重试'}, 403)
    
    return res

@user_blue.route('/modify', methods=['POST'])
def modify():
    res = None
    # 判断登陆状态
    cooike_user = request.cookies.get('user')
    if not cooike_user or cooike_user not in session:
        return make_response({'state': 'fail', 'msg': '未登录'}, 401)

    # 获取表单数据
    form_user = request.form.get('user')
    form_pwd = request.form.get('pwd')
    # 组织数据
    user, encryption = None, True
    if form_user and form_pwd:
        user = User(form_user, form_pwd)
    elif form_user:
        encryption = False
        user = User(form_user, session.get(cooike_user)['pwd'])
    elif form_pwd:
        user = User(cooike_user, form_pwd)
    else:
        return make_response({'state': 'fail', 'msg': '用户名和密码不能同时为空'}, 403)
    user.id = session.get(cooike_user)['id']
    # 提交数据库
    result = userdb.modify(user, encryption)
    if hasattr(result, 'errmsg'):
        res = make_response({'state': 'fail', 'msg': result.errmsg}, 403)
    else:
        # 修改成功
        res = make_response({'state': 'ok', 'msg': '修改成功'}, 200)
        if form_user:
            # 修改了用户名则重设会话
            session[form_user] = {'id': result.id, 'pwd': result.pwd}
            session.pop(cooike_user)
            res.set_cookie('user', result.user)
        else:
            session[cooike_user] = {'id': result.id, 'pwd': result.pwd}
        session.permanent = True

    return res

@user_blue.route('/score', methods=['GET', 'POST'])
def score():
    res = None
    cooike_user = request.cookies.get('user')
    if not cooike_user or cooike_user not in session:
        return make_response({'state': 'fail', 'msg': '请登录后操作'}, 401)

    if request.method == 'GET':
        # 查询
        result = userdb.query_all_and_user(User(cooike_user, 'None'))
        if result[0] and len(result[0]) > 0 and result[1] and len(result[1]) > 0:
            # 查询成功, 构造 dict
            dict = {
                'state': 'ok',
                'msg': '查询成功',
                'length': len(result[0]),
                'list': [],
                'user': {
                    'user': result[1]['user'],
                    'score': result[1]['score'],
                    'rank': result[1]['rank']
                }
            }
            for row in result[0]:
                dict['list'].append({'user': row['user'], 'score': row['score'], 'rank': row['rank']})
            res = make_response(jsonify(dict), 200)
        else:
            res = make_response({'state': 'fail', 'msg': '查询失败'}, 500)

    if request.method == 'POST':
        # 修改
        score = request.form.get('score')
        _user = User(cooike_user, 'None', score)
        _user.id = session.get(cooike_user)['id']
        result = userdb.modify_score(_user)
        if result['state']:
            # 修改成功
            result['state'] = 'ok'
            res = make_response(result, 200)
        else:
            result['state'] = 'fail'
            res = make_response(result, 403)

    return res

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import request, render_template
from www import app
from www.functions import *


@app.route('/')
def root():
    return render_template('/index.html')


@app.route('/login', methods=['POST'])
def login():
    # 响应登录页
    if request.method == 'GET':
        return render_template('/login.html')

    # 查询数据, 验证登陆信息
    if request.method == 'POST':
        # 获取表单数据
        uname = request.form.get('uname')
        pwd = request.form.get('pwd')

        # 插入数据库
        result = insert(3, uname, pwd, 0)
        if result['state']:
            return construct_response(200, '注册成功')
        else:
            return construct_response(304, f'注册失败, {result["msg"]}')


@app.route('/regist', methods=['POST'])
def regist():
    # 响应注册页
    if request.method == 'GET':
        return render_template('/regist.html')

    # 向数据库添加数据
    if request.method == 'POST':
        # 获取表单数据
        uname = request.form.get('uname')
        pwd = request.form.get('pwd')

        # 插入数据库
        result = insert(3, uname, pwd, 0)
        if result['state']:
            return construct_response(200, '注册成功')
        else:
            return construct_response(304, f'注册失败, {result["msg"]}')

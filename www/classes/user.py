#!/usr/bin/env python
# -*- coding: utf-8 -*-
class User:
    def __init__(self, user, pwd, score=0):
        if not user or not pwd:
            raise ValueError('值错误: 用户名和密码不能为空.')
        if not isinstance(score, int):
            try:
                score = int(score)
            except ValueError:
                raise TypeError('类型错误: 分数必须为整数.')
        self.__id = -1
        self.__user = user
        self.__pwd = pwd
        self.__score = score

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
        if not isinstance(id, int) or id < 0:
            raise TypeError('类型错误: id 必须为自然数.')
        self.__id = id
        return self

    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, user):
        if not user:
            raise ValueError('值错误: 用户名不能为空.')
        self.__user = str(user)

    @property
    def pwd(self):
        return self.__pwd

    @pwd.setter
    def pwd(self, pwd):
        if not pwd:
            raise ValueError('值错误: 密码不能为空.')
        self.__pwd = str(pwd)

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, score):
        if not isinstance(score, int):
            try:
                score = int(score)
            except ValueError:
                raise TypeError('类型错误: 分数必须为整数.')
        self.__score = score
    
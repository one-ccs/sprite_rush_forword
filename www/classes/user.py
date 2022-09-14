#!/usr/bin/env python
# -*- coding: utf-8 -*-
class User:
    def __init__(self, uname, pwd, score=0):
        if not uname or not pwd:
            raise ValueError('值错误: 用户名和密码不能为空.')
        if not isinstance(score, int) or score < 0:
            raise TypeError('类型错误: 分数必须为自然数.')
        self.__id = None
        self.__uname = uname
        self.__pwd = pwd
        self.__score = score

    @property
    def uname(self):
        return self.__uname

    @uname.setter
    def uname(self, uname):
        if not uname:
            raise ValueError('值错误: 用户名不能为空.')
        self.__uname = str(uname)

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
        if not isinstance(score, int) or score < 0:
            raise TypeError('类型错误: 分数必须为自然数.')
        self.__score = score
    
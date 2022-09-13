#!/usr/bin/env python
# -*- coding: utf-8 -*-
from www import app

__author__ = 'one-ccs'
__version__ = '0.0.1'
__port__ = 9527


if __name__ == '__main__':
    print(f'作者: {__author__}')
    print(f'邮箱: {__author__}@foxmail.com')
    print(f'版本: {__version__}')
    print('编译时间: 2022-09-13')
    print()
    app.run(port=9527, debug=True)

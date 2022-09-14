#!/usr/bin/env python
# -*- coding: utf-8 -*-
from views import errorhandle_blue

@errorhandle_blue.errorhandler(Exception)
def error_404(e):
    print('捕获错误')
    return '捕获错误'

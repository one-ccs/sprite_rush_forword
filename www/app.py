#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template
from datetime import timedelta
from classes.userdb import UserDB

app = Flask(__name__)
userdb = UserDB('../db/user.db')

app.config['SECRET_KEY'] = 'hard to gusss'
# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=1800)


@app.route('/')
def root():
    return render_template('/index.html')


from views import errorhandle_blue
from views import user_blue

app.register_blueprint(errorhandle_blue)
app.register_blueprint(user_blue)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9527, debug=True)

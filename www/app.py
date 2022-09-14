#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def root():
    return render_template('/index.html')


from views import user_blue

app.register_blueprint(user_blue)


if __name__ == '__main__':
    app.run(port=9527, debug=True)
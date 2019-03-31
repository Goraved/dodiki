#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import date

from flask import Flask, render_template

from generation import generate_list

app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')


@app.route("/")
def main():
    day_list = generate_list(date(2019, 4, 4), 0)
    return render_template('index.html')


if __name__ == "__main__":
    app.run()

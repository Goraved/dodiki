#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import date

from flask import Flask, render_template
from werkzeug.utils import redirect

from data import set_passed_rehearsals
from generation import generate_list, get_future_rehearsals, cancel_rehearsal

app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')


@app.route("/")
def main():
    set_passed_rehearsals()
    rehearsals = get_future_rehearsals()
    return render_template('index.html', today=rehearsals[0], rehearsals=rehearsals)


@app.route("/generate")
def generate_days():
    # TODO add input form
    day_list = generate_list(date.today(), 1, False)
    return redirect("/")


@app.route("/cancel/<rehearsal_id>")
def cancel(rehearsal_id):
    cancel_rehearsal(int(rehearsal_id))
    return redirect("/")


if __name__ == "__main__":
    app.run()

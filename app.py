#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime

from flask import Flask, render_template, request
from werkzeug.utils import redirect

from data import set_passed_rehearsals, get_members, swap_rehearsal_members
from generation import generate_list, get_future_rehearsals, cancel_rehearsal

app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')


@app.route("/")
def main():
    set_passed_rehearsals()
    rehearsals = get_future_rehearsals()
    members = get_members()
    return render_template('index.html', today=rehearsals[0], rehearsals=rehearsals, members=members)


@app.route("/generate", methods=['POST'])
def generate_days():
    member = int(request.form['member'])
    try:
        half = bool(request.form['half'])
    except:
        half = False
    date_from = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
    day_list = generate_list(date_from, member, half)
    return redirect("/")


@app.route("/swap", methods=['POST'])
def swap():
    swap_ids = request.form.getlist('swap')
    swap_rehearsal_members(swap_ids)
    return redirect("/")


@app.route("/cancel/<rehearsal_id>")
def cancel(rehearsal_id):
    cancel_rehearsal(int(rehearsal_id))
    return redirect("/")


if __name__ == "__main__":
    app.run()

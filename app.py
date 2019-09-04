#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime

from flask import Flask, render_template, request
from flask.json import jsonify
# from flask_swagger_ui import get_swaggerui_blueprint
# from flask_restplus import Resource, Api
from werkzeug.utils import redirect

from data import set_passed_rehearsals, get_members, swap_rehearsal_members
from generation import generate_list, get_future_rehearsals, cancel_rehearsal

SWAGGER_URL = 'swagger'
app = Flask(__name__)
# api = Api(app)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')


@app.route("/")
def main():
    set_passed_rehearsals()
    rehearsals = get_future_rehearsals()
    members = get_members()
    return render_template('index.html', today=rehearsals[0], rehearsals=rehearsals, members=members)


@app.route("/get_rehearsals", methods=['GET'])
def get_rehearsals_endpoint():
    set_passed_rehearsals()
    return jsonify({'rehearsals': get_future_rehearsals()})


@app.route("/get_members", methods=['GET'])
def get_members_endpoint():
    return jsonify({'members': get_members()})


@app.route("/generate", methods=['POST'])
def generate_days_endpoint():
    member = int(request.form['member'])
    try:
        half = bool(request.form['half'])
    except:
        half = False
    date_from = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
    day_list = generate_list(date_from, member, half)
    return redirect("/")


@app.route("/swap", methods=['POST'])
def swap_endpoint():
    swap_ids = request.form.getlist('swap')
    swap_rehearsal_members(swap_ids)
    return redirect("/")


@app.route("/cancel/<rehearsal_id>")
def cancel_endpoint(rehearsal_id):
    cancel_rehearsal(int(rehearsal_id))
    return redirect("/")


if __name__ == "__main__":
    app.run()

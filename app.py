#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from datetime import datetime

from flask import Flask, render_template, request
from flask.json import jsonify

from data import set_passed_rehearsals, get_members, swap_rehearsal_members
from generation import generate_list, get_future_rehearsals, cancel_rehearsal
from verify import requires_auth

# from flask_swagger_ui import get_swaggerui_blueprint
# from flask_restplus import Resource, Api

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


@app.route("/generate", methods=['GET', 'POST'])
@requires_auth
def generate_days_endpoint():
    _data = request.data.decode()
    obj = json.loads(_data)
    member = int(obj['member'])
    try:
        half = bool(obj['half'])
    except:
        half = False
    date_from = datetime.strptime(obj['date'], '%Y-%m-%d').date()
    generate_list(date_from, member, half)
    rehearsals = get_future_rehearsals()
    for i in rehearsals:
        i["date"] = str(i["date"])
    return str(rehearsals).replace("'", '"')


@app.route("/swap", methods=['GET', 'POST'])
@requires_auth
def swap_endpoint():
    swap_ids = request.data.decode().split(",")
    swap_rehearsal_members(swap_ids)
    rehearsals = get_future_rehearsals()
    for i in rehearsals:
        i["date"] = str(i["date"])
    return str(rehearsals).replace("'", '"')


@app.route("/cancel/<rehearsal_id>", methods=['GET', 'POST'])
@requires_auth
def cancel_endpoint(rehearsal_id):
    cancel_rehearsal(int(rehearsal_id))
    rehearsals = get_future_rehearsals()
    for i in rehearsals:
        i["date"] = str(i["date"])
    return str(rehearsals).replace("'", '"')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title='404'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('500.html', title='500'), 500


if __name__ == "__main__":
    app.run()

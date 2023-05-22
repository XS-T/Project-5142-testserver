import binascii
from json_tables import JSONTable
import threading

jt = JSONTable('table.json')
jt.load()

import requests.status_codes
from flask import Flask, jsonify, request, abort
from crewco_api.api import API

api = API()

app = Flask(__name__)


def auth_server():
    @app.route('/api/auth', methods=['POST'])
    def auth():
        data = request.get_json()  # Retrieve JSON data from the request
        try:
            name = api.decrypt(data['name'])
            key = api.decrypt(data['key'])
            print(name)
            print(key)
        except binascii.Error:
            abort(500)
        names = ["admin"]
        keys = ["password"]

        # Perform your encryption logic here based on the received data

        # Example encryption logic using a mock function
        if name in names and key in keys:
            response = {"status": "ok"}
            return jsonify(response)
        else:
            print(f"Name:{name},Key:{key}")
            abort(500)


def lookup_server():
    @app.route('/api/lookup', methods=['POST'])
    def lookup():
        data = request.get_json()  # Retrieve JSON data from the request
        try:
            name = api.decrypt(data['name'])
        except binascii.Error:
            abort(500)
        return jt.lookup(name)


auth_thread = threading.Thread(target=auth_server)
lookup_thread = threading.Thread(target=lookup_server)

auth_thread.start()
lookup_thread.start()

app.run(debug=True)

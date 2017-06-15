from flask import jsonify
from flask_restful import Resource

import docker

class Info(Resource):

    def get(self):
        client = docker.from_env()
        res = client.info()
        return jsonify(results = res)

class Version(Resource):

    def get(self):
        client = docker.from_env()
        res = client.version()
        return jsonify(results = res)

class Ping(Resource):

    def get(self):
        client = docker.from_env()
        res = client.ping()
        return jsonify(results = res)
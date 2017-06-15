from flask import jsonify
from flask_restful import Resource, reqparse
import docker

class Container(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('tag')
        self.parser.add_argument('cmd')
        self.client = docker.from_env()

    def post(self):
        """
        Run from an image
        :return:
        """
        args = self.parser.parse_args()
        tag = args['tag']
        cmd = args['cmd']
        stdout = self.client.containers.run(tag, cmd)
        return jsonify(results=stdout)



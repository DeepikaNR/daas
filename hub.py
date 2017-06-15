from flask import jsonify, request, abort
from flask_restful import Resource, reqparse

import docker
from docker.errors import APIError


class HubPush(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('image_name')     # ubuntu:v1. If no version given, latest is used
        self.parser.add_argument('repo_name')      # deepikarvce/ubuntu
        self.parser.add_argument('tag')            # : v1
        self.client = docker.from_env()

    def post(self):
        args = self.parser.parse_args()
        image_name = args['image_name']
        repo_name = args['repo_name']
        tag = args['tag']


        auth = request.authorization
        if not auth:
            print "No authentication header"
            abort(401)
        try:
            self.client.login(auth.username, auth.password)
        except APIError:
            print "Incorrect docker credentials"
            abort(401)

        image_obj = self.client.images.get(image_name)
        image_obj.tag(repo_name, tag)
        res = []

        for line in self.client.images.push(repo_name + ":" + tag, stream = True):
            print line
            res.append(line)

        return jsonify(results=res)

class HubPull(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name')
        self.client = docker.from_env()

    def post(self):
        args = self.parser.parse_args()
        name = args['name']

        image = self.client.images.pull(name)
        res = {
            'id': image.id.split(':')[-1][0:12],
            'name': image.tags,
            'Size': image.attrs['Size']
        }
        return jsonify(results=res)

class HubSearch(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('keyword')     # ubuntu:v1. If no version given, latest is used
        self.client = docker.from_env()

    def get(self):
        args = self.parser.parse_args()
        keyword = args['keyword']
        list_of_dicts = self.client.images.search(keyword)
        return jsonify(results = list_of_dicts)

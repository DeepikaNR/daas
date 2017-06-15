from flask import jsonify
from flask_restful import Resource, reqparse

import werkzeug
from werkzeug.utils import secure_filename
import docker
import os

from constants import UPLOAD_FOLDER
from util import create_docker_folder

class Images(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('id')
        self.parser.add_argument('image_name')
        self.parser.add_argument('file', type=werkzeug.datastructures.FileStorage,
                           location='files')
        self.client = docker.from_env()


    def get(self):
        args = self.parser.parse_args()
        images = self.client.images.list()
        images_res = None
        id = args['id']
        if id is None:
            images_res = []
            for image in images:
                images_res.append({
                    'id': image.id.split(':')[-1][0:12],
                    'name': image.tags,
                    'Size': image.attrs['Size'],
                    'Containers': image.attrs['Containers']
                })
        else:

            for image in images:
                if id == image.id.split(':')[-1][0:12]:
                    images_res = {
                        'id': id,
                        'name': image.tags,
                        'Size': image.attrs['Size'],
                        'Containers': image.attrs['Containers']
                    }

        return jsonify(results=images_res)

    def post(self):
        # build an image
        args = self.parser.parse_args()
        zip_file = args['file']             # wrapper for the entire file
        image_name = args['image_name']     # ubuntu:v1. If no version given, latest is used
        res = {}

        filename = secure_filename(zip_file.filename)
        print "filename=" + filename
        zip_file.save(os.path.join(UPLOAD_FOLDER, filename))

        # create a new dir with the untarred contents
        docker_path = create_docker_folder(filename)

        # build image
        image = self.client.images.build(path=docker_path, tag=image_name)

        image_info = {
            'id': image.id.split(':')[-1][0:12],
            'name': image.tags,
            'Size': image.attrs['Size']
        }
        res['image_info'] = image_info
        return jsonify(results=res)



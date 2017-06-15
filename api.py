from flask import Flask
from flask_restful import Api

from images import Images
from containers import Container
from hub import HubPush, HubSearch, HubPull
from client import Version, Info, Ping


if __name__ == '__main__':
    app = Flask(__name__)
    api = Api(app, catch_all_404s=True)

    api.add_resource(Images, '/image')
    api.add_resource(Container, '/container')
    api.add_resource(HubSearch, '/hub/search')
    api.add_resource(HubPush, '/hub/push')
    api.add_resource(HubPull, '/hub/pull')
    api.add_resource(Version, '/version')
    api.add_resource(Info, '/info')
    api.add_resource(Ping, '/ping')
    api.add_resource(Recommender, '/recommender')


    app.run(debug=True)


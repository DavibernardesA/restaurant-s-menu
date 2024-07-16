from flask import Flask
from routes import app_routes


def create_app():
    app = Flask(__name__)
    return app

create_app().register_blueprint(app_routes)

if __name__ == '__main__':
    create_app().run()

from flask import Flask
from src.routes import app_routes

def create_app():
    app = Flask(__name__)
    app.register_blueprint(app_routes)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

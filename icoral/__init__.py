from flask import Flask
from icoral.blueprints.home import home_bp

def create_app(config_name=None):
    app=Flask(__name__)
    app.register_blueprint(home_bp)

    return app



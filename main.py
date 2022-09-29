import os
from flask import Flask
from flask_restful import Resource, Api
from application import config
from application.config import LocalDevelopmentConfig
from application.database import db

app = None
api = None

def create_app():
    app = Flask(__name__, template_folder="templates")
    app.secret_key = 'Secret Key'
    if os.getenv('ENV', "development") == "production":
      raise Exception("Currently no production config is setup.")
    else:
      print("Staring Local Development")
      app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    api = Api(app)
    app.app_context().push()
    return app, api

app, api = create_app()

# Import all the controllers so they are loaded
from application.controllers import *


from application.api import ListAPI, CardAPI
api.add_resource(ListAPI, "/api/lists/<user_id>", "/api/createlist/<user_id>", "/api/deletelist/<list_id>", "/api/updatelist/<list_id>")
api.add_resource(CardAPI, "/api/cards/<list_id>", "/api/createcard/<list_id>", "/api/deletecard/<card_id>", "/api/updatecard/<card_id>")

if __name__ == '__main__':
  # Run the Flask app
  app.run()

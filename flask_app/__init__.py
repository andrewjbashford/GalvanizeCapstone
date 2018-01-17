from flask import Flask

app = Flask(__name__)

from flask_app import main
import recommender_tasks

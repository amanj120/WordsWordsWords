from flask import Flask
from flask_pymongo import PyMongo


app = Flask(__name__,
            static_folder='./public',
            template_folder='./static')
app.config.from_object('configurations.DevelopmentConfig')
mongo = PyMongo(app)


import templates.WordsWordsWords.views

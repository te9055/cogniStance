from flask import Flask

from api.api_functions import *

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello World!"


@app.route("/ner")
def ner():
    result = get_ner_for_data()
    return result


@app.route("/usas")
def usas():
    result = get_usas_for_data()
    return result

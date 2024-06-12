from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin

from api.api_functions import *

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/")
def home():
    return "Hello World!"


@app.route("/system-check")
def test():
    return "Success"


@app.route('/ner', methods=['POST'])
def ner():
    request_data = request.get_json()
    page = request_data['page']
    result = get_ner_for_data(page)
    return result


@app.route("/usas")
def usas():
    request_data = request.get_json()
    page = request_data['page']
    result = get_usas_for_data(page)
    return result

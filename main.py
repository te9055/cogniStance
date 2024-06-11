from flask import Flask
from flask import request

from api.api_functions import *

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello World!"


@app.route("/system-check")
def test():
    return "Success"


@app.route('/ner', methods=['POST'])
def ner():
    request_data = request.form.to_dict()
    page = request_data['page']
    result = get_ner_for_data(page)
    return result


@app.route("/usas")
def usas():
    result = get_usas_for_data()
    return result

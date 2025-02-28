from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin

from api.api_functions import *

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/")
def home():
    return "Success!"


@app.route("/system-check")
def test():
    return "Success"


@app.route("/ner", methods=['POST'])

def ner():
    request_data = request.get_json()
    page = request_data['page']
    result = get_ner_for_data(page)
    return result


@app.route("/translation", methods=['POST'])

def translate():
    request_data = request.get_json()
    page = request_data['page']
    result = get_translation_for_data(page)
    return result


@app.route("/usas", methods=['POST'])
def usas():
    request_data = request.get_json()
    page = request_data['page']
    result = get_usas_for_data(page)

    return result

@app.route("/usasFine", methods=['POST'])
def usasFine():
    request_data = request.get_json()
    page = request_data['page']
    result = get_usasFine_for_data(page)

    return result

@app.route("/sentiment", methods=['POST'])
def sentiment():

    request_data = request.get_json()
    page = request_data['page']
    result = get_sentiment_for_data(page)

    return result

@app.route("/collocation", methods=['POST'])
def collocation():

    request_data = request.get_json()
    page = request_data['page']
    result = get_collocation_for_data(page)

    return result

@app.route("/concordance", methods=['POST'])
def concordance():

    request_data = request.get_json()
    page = request_data['page']
    result = get_concordance_for_data(page)

    return result

@app.route("/multidatasets", methods=['POST'])
def multidatasets():

    #request_data = request.get_json()
    #page = request_data['page']
    result = run_multidatasets_all()

    return result

@app.route("/neroverall", methods=['POST'])
def neroverall():

    request_data = request.get_json()
    page = request_data['page']
    result = run_neroverall_all(page)

    return result

@app.route("/upload", methods=['POST'])
def upload():

    request_data = request.get_json()
    page = request_data['page']
    result = run_upload_all(page)

    return result

@app.route("/getdataset", methods=['POST'])
def getdataset():
    request_data = request.get_json()
    page = request_data['page']
    result = get_dataset_all(page)

    return result


@app.route("/getfiles", methods=['POST'])
def getfiles():

    request_data = request.get_json()
    page = request_data['dataset_id']
    result = get_files_all(page)

    return result

@app.route("/nlpStance", methods=['POST'])
def nlp_stance():

    request_data = request.get_json()

    result = run_nlp_stance(
        table=request_data['table'],
        dataset_id=request_data['dataset_id']
    )

    return result

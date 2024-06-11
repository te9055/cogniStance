from flask import make_response, jsonify

from func.ner.ner import *
from func.usas.usas import *


# Perform NER on a file
# TAKES XML text page
# Returns NER results
def get_ner_for_data(page):
    result = run_ner_on_text(page)

    if result["code"] == "SUCCESS":
        return make_response(jsonify(result), 201)

    return make_response(jsonify(result), 400)


def get_usas_for_data():
    result = run_usas_on_text()
    return result

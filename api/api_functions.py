from flask import make_response, jsonify

from func.ner.ner import *
from func.sentiment.sentiment import *
from func.translation.translation import run_translation_on_text
from func.usas.usas import *
from func.collocation.collocation import *
from func.concordance.concordance import *
from func.mutlidatasets.multidatasets import *
from func.neroverall.neroverall import *

# Perform NER on a file
# TAKES XML text page
# Returns NER results
def get_ner_for_data(page):
    result = run_ner_on_text(page)

    if result["code"] == "SUCCESS":
        return make_response(jsonify(result), 201)

    return make_response(jsonify(result), 400)

# Perform translation on a file
# TAKES XML text page
# Returns english translation results
def get_translation_for_data(page):

    result = run_translation_on_text(page)

    if result["code"] == "SUCCESS":
        return make_response(jsonify(result), 201)

    return make_response(jsonify(result), 400)


# Perform USAS analysis on a file
# TAKES XML text page
# Returns USAS results
def get_usas_for_data(page):
    result = run_usas_on_text(page)

    if result["code"] == "SUCCESS":
        return make_response(jsonify(result), 201)

    return make_response(jsonify(result), 400)


# Perform Sentiment analysis on a file
# TAKES XML text page
# Returns Sentiment results
def get_sentiment_for_data(page):
    result = run_sentiment_on_text(page)

    if result["code"] == "SUCCESS":
        return make_response(jsonify(result), 201)

    return make_response(jsonify(result), 400)

def get_collocation_for_data(page):
    result = run_collocation_on_text(page)

    if result["code"] == "SUCCESS":
        return make_response(jsonify(result), 201)

    return make_response(jsonify(result), 400)

def get_concordance_for_data(page):
    result = run_concordance_on_text(page)

    if result["code"] == "SUCCESS":
        return make_response(jsonify(result), 201)

    return make_response(jsonify(result), 400)

def run_multidatasets_all():
    result = run_multidatasets()

    if result["code"] == "SUCCESS":
        return make_response(jsonify(result), 201)

    return make_response(jsonify(result), 400)

def run_neroverall_all(page):
    result = run_neroverall_on_text(page)

    if result["code"] == "SUCCESS":
        return make_response(jsonify(result), 201)

    return make_response(jsonify(result), 400)



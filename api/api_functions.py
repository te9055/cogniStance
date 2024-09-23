from flask import make_response, jsonify

from func.ner.ner import *
from func.sentiment.sentiment import *
from func.translation.translation import run_translation_on_text
from func.usas.usas import *


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
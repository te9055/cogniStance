from flask import make_response, jsonify

from func.llm_summarization.llm_summarization import get_corpus_summary
from func.topic_extraction.topic_extraction import run_topic_extraction_on
from func.ner.ner import *
from func.sentiment.sentiment import *
from func.translation.translation import run_translation_on_text
from func.usas.usas import *
from func.collocation.collocation import *
from func.concordance.concordance import *
from func.mutlidatasets.multidatasets import *
from func.neroverall.neroverall import *
from func.usasFine.usasFine import *
from func.upload.upload import *
from func.getdataset.getdataset import *
from func.getfiles.getfiles import *
from func.getallids.getallids import *
from func.nlp_stance.nlp_stance import run_nlp_stance_on_text

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

def get_usasFine_for_data(page):
    result = run_usasFine_on_text(page)

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

def run_upload_all(page):
    result = upload_file(page)

    if result["code"] == "SUCCESS":
        return make_response(jsonify(result), 201)

    return make_response(jsonify(result), 400)

def get_dataset_all(page):
    result = get_dataset(page)

    if result["code"] == "SUCCESS":
        return make_response(jsonify(result), 201)

    return make_response(jsonify(result), 400)

def get_files_all(page):
    result = get_files(page)

    if result["code"] == "SUCCESS" or result["code"] == "EMPTY":
        return make_response(jsonify(result), 201)

    return make_response(jsonify(result), 400)


def get_dataset_ids():
    result = get_all_dataset_ids()

    if result["code"] == "SUCCESS":
        return make_response(jsonify(result), 200)

    return make_response(jsonify(result), 400)

def run_nlp_stance(table, dataset_id):
    result = run_nlp_stance_on_text(table, dataset_id)

    if result["code"] == "SUCCESS":
        return make_response(jsonify(result), 201)

    return make_response(jsonify(result), 400)

def run_llm_summarization(dataset_id):
    result = get_corpus_summary(dataset_id)

    if result["code"] == "SUCCESS":
        return make_response(jsonify(result), 201)

    return make_response(jsonify(result), 400)

def run_topic_extraction(summaries_table):
    result = run_topic_extraction_on(summaries_table)

    if result["code"] == "SUCCESS":
        return make_response(jsonify(result), 201)

    return make_response(jsonify(result), 400)

from func.ner.ner import *
from func.usas.usas import *


def get_ner_for_data():
    result = run_ner_on_text()
    return result


def get_usas_for_data():
    result = run_usas_on_text()
    return result

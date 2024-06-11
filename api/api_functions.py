from func.ner.ner import *
from func.usas.usas import *


# Perform NER on a file
# TAKES XML text page
# Returns NER results
def get_ner_for_data(page):
    result = run_ner_on_text(page)
    return result


def get_usas_for_data():
    result = run_usas_on_text()
    return result

import torch
from ckip_transformers.nlp import CkipWordSegmenter, CkipPosTagger, CkipNerChunker
from transformers import pipeline


# Perform NER on Text
def run_ner_on_text(page):
    ner_driver = CkipNerChunker(model="bert-base")

    data = []
    ner = ner_driver([page])

    for item in ner[0]:
        word = item.word
        ner = item.ner
        idx = item.idx
        obj = {"word": word, "translation": "", "ner": ner, "idx": idx}

        data.append(obj)

    result = {'output': data,'message': 'Done', 'code': 'SUCCESS'}

    return result

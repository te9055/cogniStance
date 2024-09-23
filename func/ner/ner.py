import torch
from ckip_transformers.nlp import CkipWordSegmenter, CkipPosTagger, CkipNerChunker
from transformers import pipeline
import pandas as pd

from shared.translate import translate

#page = '尼罗河 是一条流經非洲東部與北部的河流，與中非地區的剛果河、非洲南部的赞比西河以及西非地区的尼日尔河並列非洲最大的四個河流系統。'
# Perform NER on Text
def run_ner_on_text(page):
    ner_driver = CkipNerChunker(model="bert-base")


    ner = ner_driver([page])

    tags = []
    for item in ner[0]:
        word = item.word
        ner = item.ner
        #idx = item.idx

        tags.append(word+'__'+ner)


    ner_words_with_count = []
    seen_words = []
    for tag in tags:
        if tag not in seen_words:

            freq = tags.count(tag) / 1000000
            word = tag.split('__')[0]
            ner = tag.split('__')[1]
            translation = translate(word).text
            ner_words_with_count.append({"0 Word": word, "1 Translation":translation, "2 NER": ner, "3 Frequency": freq})
        seen_words.append(tag)


    data = sorted(ner_words_with_count, key=lambda x: x["3 Frequency"], reverse=True)

    result = {'output': data,'message': 'Done', 'code': 'SUCCESS'}

    return result








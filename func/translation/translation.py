import torch
from ckip_transformers.nlp import CkipWordSegmenter, CkipPosTagger, CkipNerChunker
from transformers import pipeline
import pandas as pd

from shared.translate import translate

#page = '尼罗河 是一条流經非洲東部與北部的河流，與中非地區的剛果河、非洲南部的赞比西河以及西非地区的尼日尔河並列非洲最大的四個河流系統。'
# Perform NER on Text
def run_translation_on_text(page):

    translation = '<p>Translation</p>'
    translation = translation + '<span>'
    translation = translation + translate(page).text
    translation = translation +'</span>'

    result = {'output': translation,'message': 'Done', 'code': 'SUCCESS'}

    return result








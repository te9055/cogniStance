import torch
from ckip_transformers.nlp import CkipWordSegmenter, CkipPosTagger, CkipNerChunker
from transformers import pipeline

# Perform NER on Text
def run_ner_on_text(page):
    ner_driver = CkipNerChunker(model="bert-base")
    ws_driver = CkipWordSegmenter(device=-1)

    txt = [
        "傅達仁今將執行安樂死，卻突然爆出自己20年前遭緯來體育台封殺，他不懂自己哪裡得罪到電視台。",
        "美國參議院針對今天總統布什所提名的勞工部長趙小蘭展開認可聽證會，預料她將會很順利通過參議院支持，成為該國有史以來第一位的華裔女性內閣成員。",
        "空白 也是可以的～",
    ]

    ner = ner_driver(txt)
    print(ner)
    return "hello ner"

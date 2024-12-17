import torch
from ckip_transformers.nlp import CkipWordSegmenter, CkipPosTagger, CkipNerChunker
from transformers import pipeline
import pandas as pd
from db.db_config import get_db

#from shared.translate import translate

#page = '尼罗河 是一条流經非洲東部與北部的河流，與中非地區的剛果河、非洲南部的赞比西河以及西非地区的尼日尔河並列非洲最大的四個河流系統。'
# Perform NER on Text
def run_ner_on_text(page):
    ner_driver = CkipNerChunker(model="bert-base")
    conn, cursor = get_db()
    cursor.execute('SELECT * from news;')
    res = cursor.fetchall()
    data = []
    for row in res:
        docid = row[0]
        content = row[-1].replace('\n', ' ').replace('\t', ' ')
        data.append([docid, content])

    ner_words_with_count = []
    for i in range(0, len(data)):
        id = data[i][0]
        txt = data[i][1]
        ner = ner_driver([txt])

        tags = []
        for item in ner[0]:
            word = item.word
            ner = item.ner
            tags.append(word+'__'+ner)



        seen_words = []
        for tag in tags:
            if tag not in seen_words:

                freq = tags.count(tag) / 1000
                word = tag.split('__')[0]
                ner = tag.split('__')[1]
                #translation = translate(word).text
                if ner == 'PERSON':
                    ner_words_with_count.append({"0 Word": word, "1 NER": ner, "2 Frequency": freq})
            seen_words.append(tag)


        perdoc = sorted(ner_words_with_count, key=lambda x: x["2 Frequency"], reverse=True)[:30]


    result = {'output': perdoc,'message': 'Done', 'code': 'SUCCESS'}

    return result












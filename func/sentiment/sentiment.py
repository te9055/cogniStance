from textblob.en import sentiment
from transformers import (
   BertTokenizerFast,
   AutoModelForMaskedLM,
   AutoModelForCausalLM,
   AutoModelForSequenceClassification,
)

from transformers import pipeline
import re
from db.db_config import get_db

def zng(paragraph):
    for sent in re.findall(u'[^!?。\.\!\?]+[!?。\.\!\?]?', paragraph, flags=re.U):
        yield sent


def run_sentiment_on_text(page):
    conn, cursor = get_db()
    cursor.execute('SELECT * from news;')
    res = cursor.fetchall()
    data = []
    sentiments = []
    for row in res:
        docid = row[0]
        content = row[-1].replace('\n', ' ').replace('\t', ' ')
        data.append([docid, content])

    allsentences = []
    for i in range(0, len(data)):
        txt = data[i][1]
        pagesList = list(zng(txt))
        allsentences.append(pagesList)

    allsentences = [x for xs in allsentences for x in xs]
    tokenizer = BertTokenizerFast.from_pretrained('bardsai/finance-sentiment-zh-base')
    model = AutoModelForSequenceClassification.from_pretrained('bardsai/finance-sentiment-zh-base')
    nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
    counts = dict()
    for p in allsentences:
        res = nlp(p)[0]['label']
        counts[res] = counts.get(res, 0) + 1

    if 'negative' not in counts.keys():
        counts['negative'] = 0


    for k in counts.keys():
        sentiments.append({"0 Sentiment": k, "1 Count": counts[k]})

    sentiments = sorted(sentiments, key=lambda x: x["1 Count"], reverse=True)
    result = {'output': sentiments, 'message': 'Done', 'code': 'SUCCESS'}

    return result







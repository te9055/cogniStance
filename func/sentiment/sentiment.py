from textblob.en import sentiment
from transformers import (
   BertTokenizerFast,
   AutoModelForMaskedLM,
   AutoModelForCausalLM,
   AutoModelForSequenceClassification,
)

from transformers import pipeline
import re

def zng(paragraph):
    for sent in re.findall(u'[^!?。\.\!\?]+[!?。\.\!\?]?', paragraph, flags=re.U):
        yield sent

#page = '尼罗河 是一条流經非洲東部與北部的河流，與中非地區的剛果河、非洲南部的赞比西河以及西非地区的尼日尔河並列非洲最大的四個河流系統。尼罗河 是一条流經非洲東部與北部的河流，與中非地區的剛果河、非洲南部的赞比西河以及西非地区的尼日尔河並列非洲最大的四個河流系統。'
def run_sentiment_on_text(page):

    pagesList = list(zng(page))
    tokenizer = BertTokenizerFast.from_pretrained('bardsai/finance-sentiment-zh-base')
    model = AutoModelForSequenceClassification.from_pretrained('bardsai/finance-sentiment-zh-base')
    nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
    counts = dict()
    for p in pagesList:
        res = nlp(p)[0]['label']
        counts[res] = counts.get(res, 0) + 1

    sentiments = []
    for k in counts.keys():
        sentiments.append({"Sentiment": k, "Count": counts[k]})

    result = {'output': sentiments, 'message': 'Done', 'code': 'SUCCESS'}
    return result


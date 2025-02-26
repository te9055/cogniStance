import spacy
import math
#from shared.translate import translate
import nltk
from nltk.collocations import TrigramCollocationFinder
from nltk.metrics import TrigramAssocMeasures
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from db.db_config import get_db


def run_collocation_on_text(page):
    datasetid = page.split('><p>')[0].replace('<div id=', '').replace('"', '').strip()
    collocations = []

    nlp = spacy.load('zh_core_web_sm')
    conn, cursor = get_db()
    #cursor.execute('SELECT * from news;')
    cursor.execute('SELECT * from files where dataset_id = "' + datasetid + '";')
    res = cursor.fetchall()

    data = []

    for row in res:

        docid = row[0]

        content = row[-1].replace('\n', ' ').replace('\t', ' ')

        data.append([docid, content])

    corpus = []
    for i in range(0, len(data)):
        id = data[i][0]
        txt = data[i][1]
        doc = nlp(txt)



        for token in doc:
            if not token.is_stop:
                # print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,token.shape_, token.is_alpha, token.is_stop)
                corpus.append(token.text.lower())


    biagram_collocation = BigramCollocationFinder.from_words(corpus)
    #biagram_collocation.apply_freq_filter(3)
    #trigram_collocation = TrigramCollocationFinder.from_words(corpus)
    #trigram_collocation.apply_freq_filter(3)


    scoredbigrams = biagram_collocation.score_ngrams(BigramAssocMeasures().likelihood_ratio)
    bigramterms = []
    for j in scoredbigrams:
        jstr = " ".join(b for b in j[0])
        bigramterms.append(jstr)

    #scoretrigrams = trigram_collocation.score_ngrams(TrigramAssocMeasures().likelihood_ratio)
    #allscores = scoredbigrams+scoretrigrams
    for item in scoredbigrams:
        itemstr = " ".join(i for i in item[0])
        if '部' in itemstr:
            itemstrnew = itemstr.replace('部','').strip().replace(' ','')
            #translation = translate(itemstr.replace('部','').strip()).text.lower()
            #print(translation)
            #print('--------------')
            score = round(item[1],3)

            freq = bigramterms.count(itemstr)/ 1000
            collocations.append({"0 Collocate": itemstrnew , "1 LogRatio": score, "2 Frequency":freq})


    collocationsorted = sorted(collocations, key=lambda x: (x["1 LogRatio"],x["2 Frequency"]), reverse=True)[:10]

    result = {'output': collocationsorted, 'message': 'Done', 'code': 'SUCCESS'}
    return result





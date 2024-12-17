import spacy
from shared.translate import translate
from wasabi import Printer
from spacy.matcher import PhraseMatcher
from db.db_config import get_db
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures



def collocations():
    collocations = []

    nlp = spacy.load('zh_core_web_sm')
    conn, cursor = get_db()
    cursor.execute('SELECT * from news;')
    res = cursor.fetchall()

    data = []

    for row in res:
        docid = row[0]

        content = row[-1].replace('\n', ' ').replace('\t', ' ')

        data.append([docid, content])

    corpus = []
    for i in range(0, len(data)):
        txt = data[i][1]
        doc = nlp(txt)

        for token in doc:
            if not token.is_stop:
                # print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,token.shape_, token.is_alpha, token.is_stop)
                corpus.append(token.text.lower())

    biagram_collocation = BigramCollocationFinder.from_words(corpus)


    scoredbigrams = biagram_collocation.score_ngrams(BigramAssocMeasures().likelihood_ratio)
    bigramterms = []
    for j in scoredbigrams:
        jstr = " ".join(b for b in j[0])
        bigramterms.append(jstr)

    # scoretrigrams = trigram_collocation.score_ngrams(TrigramAssocMeasures().likelihood_ratio)
    # allscores = scoredbigrams+scoretrigrams
    for item in scoredbigrams:
        itemstr = " ".join(i for i in item[0])
        if '部' in itemstr:
            itemstrnew = itemstr
            translation = translate(itemstr).text.lower()
            # print(translation)
            # print('--------------')
            score = round(item[1], 3)

            freq = bigramterms.count(itemstr) / 1000
            collocations.append({"0 Collocate": itemstrnew, "1 LogRatio": score, "2 Frequency": freq})

    collocationsorted = sorted(collocations, key=lambda x: (x["1 LogRatio"], x["2 Frequency"]), reverse=True)[:10]

    terms = [d['0 Collocate'] for d in collocationsorted]
    return terms


def run_concordance_on_text(page):
    nlp = spacy.load('zh_core_web_sm')
    conn, cursor = get_db()
    cursor.execute('SELECT * from news;')
    res = cursor.fetchall()
    data = []
    for row in res:
        docid = row[0]
        content = row[-1].replace('\n', ' ').replace('\t', ' ')
        data.append([docid, content])

    concordances = []
    terms = collocations()
    for i in range(0, len(data)):
        id = data[i][0]
        txt = data[i][1]
        doc = nlp(txt)


        matcher = PhraseMatcher(nlp.vocab,attr='LOWER')
        patterns = [nlp.make_doc(term) for term in terms]
        matcher.add("TermCollocations", patterns)

        matches = matcher(doc)
        match = Printer()
        for j, start, end in matches:
            perecedingSlice = doc[start - 20: start].text
            if '。' in perecedingSlice:
                perecedingSlice = perecedingSlice.split('。')[1]
            else:
                perecedingSlice = perecedingSlice.strip()


            #perecedingSliceTr = clean(translate(doc[start - 20: start]).text)
            matchedTerm = doc[start:end].text
            #matchedTerm = doc[start:end].text
            matchedTermTr = match.text(translate(doc[start:end].text).text, color='red', no_print=True)
            #matchedTermTr = match.text(translate(doc[start:end].text).text)
            followingSlice = doc[end:end + 20].text
            #followingSliceTr = clean(translate(doc[end:end + 20]).text)

            #context = perecedingSlice+', '+matchedTerm+', '+followingSlice

            #contextTr = perecedingSliceTr+', '+matchedTermTr+', '+followingSliceTr
            #concordances.append({"0 Term": escapeAnscii(matchedTerm), "1 Eng": escapeAnscii(matchedTermTr), "2 Context":escapeAnscii(context), "3 Context Eng":escapeAnscii(contextTr)})
            concordances.append({"0 Preceded By":perecedingSlice,"1 Term": matchedTerm, "2 Followed By": followingSlice})


    result = {'output': concordances, 'message': 'Done', 'code': 'SUCCESS'}

    return result




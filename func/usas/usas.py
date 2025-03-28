import spacy
from db.db_config import get_db


# Perform USAS on Text
#page = '尼罗河 是一条流經非洲東部與北部的河流，與中非地區的剛果河、非洲南部的赞比西河以及西非地区的尼日尔河並列非洲最大的四個河流系統。'


def run_usas_on_text(page):
    print('usasoverall page old: ', page)
    datasetid = page.split('><p>')[0].replace('<div id=', '').replace('"', '').strip()
    print('usas overall datasetid: ', datasetid)
    d = {}
    with open('func/usas/usas_overall.txt') as f:
        for line in f:
            lineL = line.replace('\n', '').split(' ', 1)
            key = lineL[0].strip()
            val = lineL[1].strip()
            d[key] = val


    # We exclude the following components as we do not need them.
    nlp = spacy.load('zh_core_web_sm', exclude=['parser', 'ner'])
    # Load the Chinese PyMUSAS rule-based tagger in a separate spaCy pipeline
    chinese_tagger_pipeline = spacy.load('cmn_dual_upos2usas_contextual')
    # Adds the Chinese PyMUSAS rule-based tagger to the main spaCy pipeline
    nlp.add_pipe('pymusas_rule_based_tagger', source=chinese_tagger_pipeline)

    conn, cursor = get_db()
    #cursor.execute('SELECT * from news;')
    cursor.execute('SELECT * from files where dataset_id = "'+datasetid+'";')
    res = cursor.fetchall()
    data = []

    for row in res:
        docid = row[0]
        content = row[-1].replace('\n', ' ').replace('\t', ' ')
        data.append([docid, content])

    #output_doc = nlp(page)
    usas_tags_with_count = []
    tags = []
    seen_tags = []
    for i in range(0, len(data)):
        id = data[i][0]
        txt = data[i][1]
        output_doc = nlp(txt)



        for token in output_doc:
            start, end = token._.pymusas_mwe_indexes[0]
            idx = (start, end)

            for el in token._.pymusas_tags:
                el = el.split('.')[0][0]
                #obj = {"word": token.text, "USAS Tags": el, "idx": idx}
                tags.append(el)
                #data.append(obj)



        for tag in tags:
            if tag not in seen_tags:
                try:
                    freq = tags.count(tag)/1000

                    usas_tags_with_count.append({"0 Tag": tag, "1 Definition":d[tag],"2 Frequency": freq})
                except KeyError:
                    pass
            seen_tags.append(tag)

    usas_tags_with_count_sorted = sorted(usas_tags_with_count, key=lambda x: x["2 Frequency"], reverse=True)


    result = {'output': usas_tags_with_count_sorted, 'message': 'Done', 'code': 'SUCCESS'}

    return result









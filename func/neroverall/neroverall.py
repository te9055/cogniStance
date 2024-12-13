from ckip_transformers.nlp import CkipNerChunker
from db.db_config import get_db


#page = '尼罗河 是一条流經非洲東部與北部的河流，與中非地區的剛果河、非洲南部的赞比西河以及西非地区的尼日尔河並列非洲最大的四個河流系統。'
# Perform NER on Text
def run_neroverall_on_text(page):
    ner_driver = CkipNerChunker(model="bert-base")
    conn, cursor = get_db()
    cursor.execute('SELECT * from news;')
    res = cursor.fetchall()
    data = []
    for row in res:
        docid = row[0]
        content = row[-1].replace('\n', ' ').replace('\t', ' ')
        data.append([docid, content])

    ner_with_count = []
    for i in range(0,len(data)):
        id = data[i][0]
        txt = data[i][1]
        ner = ner_driver([txt])
        tags = []
        for item in ner[0]:
            word = item.word
            ner = item.ner
            tags.append(word + '__' + ner)

        ners = []

        seen_words = []
        seen_tags = []
        for tag in tags:
            if tag not in seen_words:
                ner = tag.split('__')[1].strip()

                ners.append(ner)

            seen_words.append(tag)

        for n in ners:
            if n not in seen_tags:
                freq = ners.count(n) / 1000000
                ner_with_count.append({"0 Doc Id": id, "1 NER": n, "2 Frequency": freq})

            seen_tags.append(n)

    #nerall = sorted(ner_with_count, key=lambda x: (x["0 Doc Id"],x["2 Frequency"]), reverse=True)

    result = {'output': ner_with_count,'message': 'Done', 'code': 'SUCCESS'}
    
    return result



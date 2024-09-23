import spacy


# Perform USAS on Text
#page = '尼罗河 是一条流經非洲東部與北部的河流，與中非地區的剛果河、非洲南部的赞比西河以及西非地区的尼日尔河並列非洲最大的四個河流系統。'


def run_usas_on_text(page):
    d = {}
    with open('/Users/tom/PycharmProjects/cognistance/func/usas/usas_desc.txt') as f:
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

    output_doc = nlp(page)
    #data = []

    tags = []

    for token in output_doc:
        start, end = token._.pymusas_mwe_indexes[0]
        idx = (start, end)

        for el in token._.pymusas_tags:
            #obj = {"word": token.text, "USAS Tags": el, "idx": idx}
            tags.append(el)
            #data.append(obj)

    usas_tags_with_count = []
    seen_tags = []
    for tag in tags:
        if tag not in seen_tags:
            try:
                freq = tags.count(tag)/1000000
                usas_tags_with_count.append({"0 Tag": tag, "1 Definition":d[tag],"2 Frequency": freq})
            except KeyError:
                pass
        seen_tags.append(tag)

    usas_tags_with_count = sorted(usas_tags_with_count, key=lambda x: x["2 Frequency"], reverse=True)
    result = {'output': usas_tags_with_count, 'message': 'Done', 'code': 'SUCCESS'}

    return result


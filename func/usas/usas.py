import spacy


# Perform USAS on Text
def run_usas_on_text(page):
    # We exclude the following components as we do not need them.
    nlp = spacy.load('zh_core_web_sm', exclude=['parser', 'ner'])
    # Load the Chinese PyMUSAS rule-based tagger in a separate spaCy pipeline
    chinese_tagger_pipeline = spacy.load('cmn_dual_upos2usas_contextual')
    # Adds the Chinese PyMUSAS rule-based tagger to the main spaCy pipeline
    nlp.add_pipe('pymusas_rule_based_tagger', source=chinese_tagger_pipeline)

    output_doc = nlp(page)
    data = []

    tags = []

    print(f'Text\tPOS\tMWE start and end index\tUSAS Tags')
    for token in output_doc:
        start, end = token._.pymusas_mwe_indexes[0]
        idx = (start, end)

        for el in token._.pymusas_tags:
            obj = {"word": token.text, "Usas Tags": el, "idx": idx}
            tags.append(el)
            data.append(obj)

    res = []
    procTags = []
    for x in tags:
        if x not in procTags:
            res.append({"Tag": x, "Count": tags.count(x)})

        procTags.append(x)

    result = {'output': res, 'message': 'Done', 'code': 'SUCCESS'}
    return result

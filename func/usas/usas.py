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

    print(f'Text\tPOS\tUSAS Tags')
    for token in output_doc:
        print(f'{token.text}\t{token.pos_}\t{token._.pymusas_tags}')

    result = {'output': "Hello USAS", 'message': 'Done', 'code': 'SUCCESS'}
    return result

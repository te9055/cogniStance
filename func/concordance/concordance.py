import spacy
import math
from collections import Counter, defaultdict
from shared.translate import translate
from wasabi import Printer
from spacy.matcher import PhraseMatcher
import re

#page = '专精特新”企业，是指具有专业化、精细化、特色化、新颖化四大特征的中小企业。创新是这类企业的灵魂，足够的 研发费用投入则是开展创新的重要保障。许多尚处在成长期的“专精特新”企业，近期普遍遭遇“钱紧”难题。如何集聚 更多的资金投入研发、保持创新领先地位是这些企业近来面临的最大烦恼。“作为一家新材料研发公司，创新是我们发展的重要驱动力，只有研发投入的不断加码，企业创新发展的步伐才不会 降速。”浙江省“专精特新”企业、宁波创润新材料有限公司董事长吴景晖说，过去3年，企业在研发投入方面不遗余力，累计投入2500万元，这对企业来说不是个小数目。 今年新兴市场的研发需求十分迫切，我们一直想加快 超高纯钛及钛合金中试生产线项目 的研发进度，但苦于资金不 足。令人高兴的是，今年4月340万元存量增值税留抵税额的到账，有效缓解了企业的资金压力，加快了企业的研发 进度。”吴景晖说，目前，“超高纯钛及钛合金中试生产线项目”正在有序推进，一旦投产将缓解半导体产业的高纯钛原材料供应不足问题，提升国产溅射靶材的市场竞争力'

def calculate_pmi(bigram, p_bigram, p_word):
    word1, word2 = bigram
    return math.log2(max(p_bigram[bigram], 1e-10) / (max(p_word[word1], 1e-10) * max(p_word[word2], 1e-10)))

def escape(token: str):
    token = token.replace("&", " ")
    token = token.replace("-", " ")
    token = token.replace("<", " ")
    token = token.replace(">", " ")
    token = token.replace("\"", " ")
    token = token.replace("'", " ")
    token = token.strip()
    return token

def collocations(doc):

    corpus = []

    for token in doc:
        if not token.is_stop:
            corpus.append(escape(token.text.lower()))

    # Step 2: Calculate Frequencies
    word_freq = Counter(corpus)
    bigram_freq = Counter(zip(corpus[:-1], corpus[1:]))

    # Step 3: Calculate Probabilities
    total_words = len(corpus)
    p_word = defaultdict(float)
    p_bigram = defaultdict(float)

    for word, freq in word_freq.items():
        p_word[word] = freq / total_words

    total_bigrams = len(corpus) - 1
    all_pmi_scores = []
    for bigram, freq in bigram_freq.items():
        p_bigram[bigram] = freq / total_bigrams
        bigramstr = bigram[0] + ' ' + bigram[1]

        pmi = calculate_pmi(bigram, p_bigram, p_word)

        all_pmi_scores.append({"0 Term": bigramstr, "2 PMI Score": round(pmi, 3)})

    all_pmi_score = sorted(all_pmi_scores, key=lambda x: x["2 PMI Score"], reverse=True)
    all_pmi_score = all_pmi_score[slice(40)]
    terms = [item.get('0 Term') for item in all_pmi_score]


    return  terms

def clean(text):
    ansi_escape = re.compile(r'''
        \x1B  # ESC
        (?:   # 7-bit C1 Fe (except CSI)
            [@-Z\\-_]
        |     # or [ for CSI, followed by a control sequence
            \[
            [0-?]*  # Parameter bytes
            [ -/]*  # Intermediate bytes
            [@-~]   # Final byte
        )
    ''', re.VERBOSE)
    cltext = ansi_escape.sub('', text)

    return str(cltext)

def run_concordance_on_text(page):
    nlp = spacy.load('zh_core_web_sm')
    doc = nlp(page)
    terms = collocations(doc)
    concordances = []
    matcher = PhraseMatcher(nlp.vocab,attr='LOWER')
    patterns = [nlp.make_doc(term) for term in terms]
    matcher.add("TermCollocations", patterns)

    matches = matcher(doc)
    match = Printer()
    for i, start, end in matches:
        perecedingSlice = clean(doc[start - 7: start].text)


        perecedingSliceTr = clean(translate(doc[start - 7: start]).text)
        matchedTerm = clean(match.text(doc[start:end].text, color='red', no_print=True))
        #matchedTerm = doc[start:end].text
        matchedTermTr = clean(match.text(translate(doc[start:end].text).text, color='red', no_print=True))
        #matchedTermTr = match.text(translate(doc[start:end].text).text)
        followingSlice = clean(doc[end:end + 7].text)
        followingSliceTr = clean(translate(doc[end:end + 7]).text)

        context = perecedingSlice+', '+matchedTerm+', '+followingSlice

        contextTr = perecedingSliceTr+', '+matchedTermTr+', '+followingSliceTr
        #concordances.append({"0 Term": escapeAnscii(matchedTerm), "1 Eng": escapeAnscii(matchedTermTr), "2 Context":escapeAnscii(context), "3 Context Eng":escapeAnscii(contextTr)})
        concordances.append({"0 Term": matchedTerm, "1 Eng": matchedTermTr,"2 Context": context, "3 Context Eng": contextTr})

    print(concordances)
    result = {'output': concordances, 'message': 'Done', 'code': 'SUCCESS'}

    return result

#def main():
#    result = run_concordance_on_text(page)

#main()


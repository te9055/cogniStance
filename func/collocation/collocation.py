import spacy
import math
from collections import Counter, defaultdict
from shared.translate import translate

#page = '专精特新”企业，是指具有专业化、精细化、特色化、新颖化四大特征的中小企业。创新是这类企业的灵魂，足够的 研发费用投入则是开展创新的重要保障。许多尚处在成长期的“专精特新”企业，近期普遍遭遇“钱紧”难题。如何集聚 更多的资金投入研发、保持创新领先地位是这些企业近来面临的最大烦恼。“作为一家新材料研发公司，创新是我们发展的重要驱动力，只有研发投入的不断加码，企业创新发展的步伐才不会 降速。”浙江省“专精特新”企业、宁波创润新材料有限公司董事长吴景晖说，过去3年，企业在研发投入方面不遗余力，累计投入2500万元，这对企业来说不是个小数目。 今年新兴市场的研发需求十分迫切，我们一直想加快 超高纯钛及钛合金中试生产线项目 的研发进度，但苦于资金不 足。令人高兴的是，今年4月340万元存量增值税留抵税额的到账，有效缓解了企业的资金压力，加快了企业的研发 进度。”吴景晖说，目前，“超高纯钛及钛合金中试生产线项目”正在有序推进，一旦投产将缓解半导体产业的高纯钛原材料供应不足问题，提升国产溅射靶材的市场竞争力'

# Step 4: Calculate PMI for all Bigrams
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

def run_collocation_on_text(page):
    corpus = []

    nlp = spacy.load('zh_core_web_sm')
    doc = nlp(page)
    for token in doc:
        if not token.is_stop:

            #print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,token.shape_, token.is_alpha, token.is_stop)
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
        bigramstr = bigram[0]+' '+bigram[1]
        translation = translate(bigramstr).text.lower()
        pmi = calculate_pmi(bigram, p_bigram, p_word)

        all_pmi_scores.append({"0 Term": bigramstr,"1 Translation":translation ,"2 PMI Score": round(pmi,3)})



    all_pmi_score = sorted(all_pmi_scores, key=lambda x: x["2 PMI Score"], reverse=True)
    all_pmi_score = all_pmi_score[slice(40)]
    result = {'output': all_pmi_score, 'message': 'Done', 'code': 'SUCCESS'}
    print("PMI Scores:", all_pmi_scores)

    return result


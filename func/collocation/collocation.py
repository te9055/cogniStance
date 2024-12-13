import spacy
import math
from shared.translate import translate
from nltk.collocations import TrigramCollocationFinder
from nltk.metrics import TrigramAssocMeasures
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures


#page = '专精特新”企业，是指具有专业化、精细化、特色化、新颖化四大特征的中小企业。创新是这类企业的灵魂，足够的 研发费用投入则是开展创新的重要保障。许多尚处在成长期的“专精特新”企业，近期普遍遭遇“钱紧”难题。如何集聚 更多的资金投入研发、保持创新领先地位是这些企业近来面临的最大烦恼。“作为一家新材料研发公司，创新是我们发展的重要驱动力，只有研发投入的不断加码，企业创新发展的步伐才不会 降速。”浙江省“专精特新”企业、宁波创润新材料有限公司董事长吴景晖说，过去3年，企业在研发投入方面不遗余力，累计投入2500万元，这对企业来说不是个小数目。 今年新兴市场的研发需求十分迫切，我们一直想加快 超高纯钛及钛合金中试生产线项目 的研发进度，但苦于资金不 足。令人高兴的是，今年4月340万元存量增值税留抵税额的到账，有效缓解了企业的资金压力，加快了企业的研发 进度。”吴景晖说，目前，“超高纯钛及钛合金中试生产线项目”正在有序推进，一旦投产将缓解半导体产业的高纯钛原材料供应不足问题，提升国产溅射靶材的市场竞争力'




def clean(text):

    text = text.replace('<p>', ' ')
    text = text.replace('</p>', ' ')
    text = text.replace('<br>', ' ')
    text = text.replace('</br>', ' ')
    text = text.replace('><', ' ')
    text = text.replace('\u3000', ' ')
    text = text.replace('br', ' ')
    cltext = text.replace('\n', ' ').strip()
    return str(cltext)

def run_collocation_on_text(page):

    page = clean(page)

    corpus = []
    collocations = []

    nlp = spacy.load('zh_core_web_sm')
    doc = nlp(page)

    for token in doc:
        if not token.is_stop:
            # print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,token.shape_, token.is_alpha, token.is_stop)
            corpus.append(token.text.lower())


    biagram_collocation = BigramCollocationFinder.from_words(corpus)
    #biagram_collocation.apply_freq_filter(3)
    trigram_collocation = TrigramCollocationFinder.from_words(corpus)
    #trigram_collocation.apply_freq_filter(3)

    scoredbigrams = biagram_collocation.score_ngrams(BigramAssocMeasures().likelihood_ratio)[:10]

    scoretrigrams = trigram_collocation.score_ngrams(TrigramAssocMeasures().likelihood_ratio)[:10]
    allscores = scoredbigrams+scoretrigrams
    for item in allscores:
        itemstr = " ".join(i for i in item[0])
        translation = translate(itemstr).text.lower()
        score = item[1]/1000000
        collocations.append({"0 Term": itemstr,"1 Translation":translation ,"2 LogRatio": score})


    collocations = sorted(collocations, key=lambda x: x["2 LogRatio"], reverse=True)


    result = {'output': collocations, 'message': 'Done', 'code': 'SUCCESS'}
    return result



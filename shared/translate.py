from googletrans import Translator


# wrapper for the googletrans library. Takes in chinese string returns english
def translate(word):
    translator = Translator()

    result = translator.translate(word, src='zh-cn', dest='en')

    return result

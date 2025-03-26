from bertopic import BERTopic
from bertopic.vectorizers import ClassTfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sentence_transformers import SentenceTransformer
from polyglot.text import Text
import jieba
import html_to_json


def tokenize_zh(text):
    words = jieba.lcut(text)
    return words


VECTORIZERS_BY_LANGUAGE = {
    'en': CountVectorizer(),
    'zh': CountVectorizer(tokenizer=tokenize_zh),
}

def get_vectorizer(summaries):
    print(summaries[0])
    lang_code = Text(summaries[0]).language.code  # This assumes that all the summaries are in the same language!
    print(lang_code)

    if lang_code in VECTORIZERS_BY_LANGUAGE:
        return VECTORIZERS_BY_LANGUAGE[lang_code]

    # If we haven't defined a specific vectorizer, use the default of CountVector
    # This works well for western languages but fails with some non-western languages (like Chinese)
    # If that's the case, you can define a language-specific vectorizer above
    return CountVectorizer()


def run_topic_extraction_on(summaries_table):
    summaries = [
        row['Summary']
        for row in html_to_json.convert_tables(summaries_table)[0]
        if 'Summary' in row
    ]

    model = SentenceTransformer('sentence-transformers/LaBSE')
    ctfidf_model = ClassTfidfTransformer(reduce_frequent_words=True)
    vectorizer = get_vectorizer(summaries)

    topic_model = BERTopic(embedding_model=model, vectorizer_model=vectorizer, ctfidf_model=ctfidf_model)
    topic_model.fit_transform(summaries)

    df = topic_model.get_topic_info()
    print(df)

    df = df[df['Topic'] >= 0]  # Ignore the -1 topic as it only contains outliers
    df = df[["Count", "Representation"]].rename(
        columns={"Representation": "0 Key Words", "Count": "1 # Documents"}
    )

    return {
        'output': df.to_dict("records"),
        'message': 'Done',
        'code': 'SUCCESS'
    }

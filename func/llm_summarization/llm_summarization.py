import re
import json
import ollama

from db.db_config import get_db

# DEFAULT_SUMMARY = "func/llm_summarization/summarization_confs/deepseek_english_summary.json"
# DEFAULT_SUMMARY = "func/llm_summarization/summarization_confs/deepseek-1_5b_english_summary.json"
DEFAULT_SUMMARY = "func/llm_summarization/summarization_confs/deepseek-1_5b_chinese_summary.json"


def deepseek_cleanup_summary(summary):
    return re.sub(r'<think>(?s:.)*</think>', '', summary).strip()


def get_llm_answer(text, conf):
    return ollama.chat(
        model=conf['model'],
        messages=[
            {
                "role": m['role'],
                "content": m['content'].format(text=text)
            }
            for m in conf['prompts']
        ]
    ).message.content


def get_summary(text, conf):
    return deepseek_cleanup_summary(get_llm_answer(text, conf))


def get_corpus_summary(dataset_id, conf_file=DEFAULT_SUMMARY):
    conn, cursor = get_db()
    cursor.execute(f'SELECT filename, content from files where dataset_id = "{dataset_id}";')
    res = cursor.fetchall()

    with open(conf_file, "r") as f:
        conf = json.load(f)

    return {
        'output': [
            {
                "0 Title": row[0],
                "1 Summary": get_summary(row[-1], conf=conf),
            }
            for row in res
        ],
        'message': 'Done',
        'code': 'SUCCESS'
    }

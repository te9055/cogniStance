import re
from db.db_config import get_db


def get_documents(dataset_id) -> list[tuple[int, str]]:
    conn, cursor = get_db()
    cursor.execute(f'SELECT id, content from files where dataset_id = "{dataset_id}";')
    res = cursor.fetchall()
    data = []

    for row in res:
        docid = row[0]
        content = row[1].replace('\n', ' ').replace('\t', ' ')
        data.append([docid, content])

    return data


def zng(paragraph):
    for sent in re.findall(u'[^!?。\.\!\?]+[!?。\.\!\?]?', paragraph, flags=re.U):
        yield sent


def get_documents_as_sentences(dataset_id) -> list[list[str]]:
    """Returns all the documents in the database as a list, where each document is formatted as a list containing
    the sentences that form that document."""
    data = get_documents(dataset_id)

    allsentences = []
    for i in range(0, len(data)):
        txt = data[i][1]
        pagesList = list(zng(txt))
        allsentences.append(pagesList)

    return allsentences


def get_all_sentences(dataset_id) -> list[str]:
    """Returns a single list with all the sentences from all the documents in the database."""
    return [x for xs in get_documents_as_sentences(dataset_id) for x in xs]

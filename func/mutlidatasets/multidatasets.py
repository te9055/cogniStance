import pandas as pd
from db.db_config import get_db



#page = '尼罗河 是一条流經非洲東部與北部的河流，與中非地區的剛果河、非洲南部的赞比西河以及西非地区的尼日尔河並列非洲最大的四個河流系統。'
# Perform NER on Text
def run_multidatasets():
    conn, cursor = get_db()
    cursor.execute('SELECT * from news;')
    res = cursor.fetchall()
    data = []
    for row in res:
        print(row)
        data.append({"0 Title": row[1], "1 Date": row[4]})





    result = {'output': data,'message': 'Done', 'code': 'SUCCESS'}

    return result

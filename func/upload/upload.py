from db.db_config import get_db

def upload_file(page):


    #filename = page.get('filename')
    #last_modified = page.get('lastModified')
    content = page.get('content')
    dataset_id = page.get("dataset_id")
    file_info = page.get("file")

    conn, cursor = get_db()
    cursor.execute("INSERT INTO files (dataset_id, filename, date, content) VALUES (?, ?, ?, ?)",
                   (dataset_id, file_info["filename"], file_info["lastModified"], file_info["content"]))
    conn.commit()
    conn.close()
    result = {'output': content, 'message': 'Done', 'code': 'SUCCESS'}
    return result

from db.db_config import get_db


def get_files(dataset_id):
    print('received page within get files: ',dataset_id)

     # Read JSON body


    if not dataset_id:
        return {"message": "Missing dataset_id", "code": "ERROR"}, 400  # Return error if missing

    conn, cursor = get_db()
    cursor.execute("SELECT filename, date FROM files WHERE dataset_id = ?", (dataset_id,))
    files = [{"title": row[0], "date": row[1]} for row in cursor.fetchall()]

    print(f"Retrieved files for dataset_id {dataset_id}: {files}")
    conn.close()

    if not files:
        print(f"No files found for dataset_id {dataset_id}")  # Log warning
        return {"files": [], "message": "No files found", "code": "EMPTY"}

    return {"files": files, "message": "Success", "code": "SUCCESS"}

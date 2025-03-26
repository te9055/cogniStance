from db.db_config import get_db

def get_all_dataset_ids():
    """Fetch all datasets and their associated files."""
    conn, cursor = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM datasets")
    datasets = cursor.fetchall()

    dataset_list = []
    for dataset in datasets:
        #print('inside get_all_dataset_ids dataset', dataset)
        dataset_id = dataset[0]
        cursor.execute("SELECT filename, date FROM files WHERE dataset_id = ?", (dataset_id,))
        files = cursor.fetchall()

        dataset_list.append({
            "dataset_id": dataset_id,
            "files": [{"title": f[0], "date": f[1]} for f in files]
        })



    conn.close()
    print('inside get_all_dataset_ids, dataset_list: ', dataset_list)
    return {"datasets": dataset_list, "message": "Success", "code": "SUCCESS"}

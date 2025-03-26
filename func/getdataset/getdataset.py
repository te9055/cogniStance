from db.db_config import get_db

def get_dataset(page):

    is_empty = page.get("is_empty", True)
    dataset_id = page.get("dataset_id")  # Check if dataset ID is provided

    conn, cursor = get_db()
    cursor = conn.cursor()

    if is_empty and not dataset_id:
        # Create a new dataset ID if table is empty and no ID exists
        cursor.execute("INSERT INTO datasets DEFAULT VALUES")
        dataset_id = cursor.lastrowid
    elif not is_empty and dataset_id:
        # If table is not empty and dataset ID exists, return it
        pass  # No need to fetch anything, just return the given dataset_id
    else:
        # If no dataset ID was provided, return the latest one in the database
        cursor.execute("SELECT id FROM datasets ORDER BY id DESC LIMIT 1")
        result = cursor.fetchone()
        dataset_id = result[0] if result else None

    conn.commit()
    conn.close()

    result = {"dataset_id": dataset_id, "message": "Done", "code": "SUCCESS"}
    return result

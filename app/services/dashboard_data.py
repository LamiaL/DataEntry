import sqlite3

def get_entries_by_date(db_path, table_name):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = f"SELECT DATE(created_at), COUNT(*) FROM {table_name} GROUP BY DATE(created_at)"
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return [{"date": row[0], "count": row[1]} for row in data]


def get_entries_by_agent(db_path, table_name):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = f"SELECT nameAgent, COUNT(*) FROM {table_name} GROUP BY nameAgent"
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return [{"agent": row[0], "count": row[1]} for row in data]

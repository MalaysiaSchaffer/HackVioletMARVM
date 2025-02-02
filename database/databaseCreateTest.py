import sqlite3

def create_connection(db_file):
    """ create a database connection to the SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)

def insert_data(conn, data):
    """ insert data into the image_labels table """
    sql = ''' INSERT INTO image_labels(image_url, ai_label, human_1_score, human_2_score, human_3_score, human_1_comment, human_2_comment, human_3_comment, ai_accuracy)
              VALUES(?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, data)
    conn.commit()
    return cur.lastrowid

def insert_multiple_records(conn, data_list):
    """ insert multiple records into the image_labels table """
    sql = ''' INSERT INTO image_labels(image_url, ai_label, human_1_score, human_2_score, human_3_score, human_1_comment, human_2_comment, human_3_comment, ai_accuracy)
              VALUES(?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    try:
        cur.executemany(sql, data_list)
        conn.commit()
    except sqlite3.Error as e:
        print(e)

def validate_data(data):
    """ validate data before insertion """
    if not all(isinstance(field, (str, int, float)) for field in data):
        raise ValueError("Invalid data types")
    return True

def query_records(conn, query):
    """ query records from the image_labels table """
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    for row in rows:
        print(row)

def update_record(conn, data):
    """ update a record in the image_labels table """
    sql = ''' UPDATE image_labels
              SET image_url = ?,
                  ai_label = ?,
                  human_1_score = ?,
                  human_2_score = ?,
                  human_3_score = ?,
                  human_1_comment = ?,
                  human_2_comment = ?,
                  human_3_comment = ?,
                  ai_accuracy = ?
              WHERE image_id = ? '''
    cur = conn.cursor()
    try:
        cur.execute(sql, data)
        conn.commit()
    except sqlite3.Error as e:
        print(e)

def delete_record(conn, image_id):
    """ delete a record from the image_labels table """
    sql = 'DELETE FROM image_labels WHERE image_id=?'
    cur = conn.cursor()
    try:
        cur.execute(sql, (image_id,))
        conn.commit()
    except sqlite3.Error as e:
        print(e)

    """ verify the inserted data """
    cur = conn.cursor()
    cur.execute("SELECT * FROM image_labels")
    rows = cur.fetchall()
    for row in rows:
        print(row)

def main():
    database = "astroannotate.db"

    sql_create_image_labels_table = """ CREATE TABLE IF NOT EXISTS image_labels (
                                        image_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        image_url TEXT NOT NULL,
                                        ai_label TEXT NOT NULL,
                                        human_1_score INTEGER,
                                        human_2_score INTEGER,
                                        human_3_score INTEGER,
                                        human_1_comment TEXT,
                                        human_2_comment TEXT,
                                        human_3_comment TEXT,
                                        ai_accuracy REAL
                                    ); """

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create image_labels table
        create_table(conn, sql_create_image_labels_table)

        # insert example data
        data = ('uploads/image1.jpg', 'cat', 1, 0, 1, 'Looks correct', 'I think it\'s a dog', 'Agree with AI', 85.0)
        insert_data(conn, data)

        # verify data
        verify_data(conn)

        # close connection
        conn.close()
    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()

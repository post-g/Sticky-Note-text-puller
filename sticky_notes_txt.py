import sqlite3
import re



def create_connection(sticky_db):
    try:
        conn = sqlite3.connect(sticky_db)
    except Error as erorr:
        print(erorr)

    return conn


def get_sticky_note_text(conn):
    cur = conn.cursor()
    cur.execute("SELECT Text FROM Note")
    rows = cur.fetchone()

    return rows 



def main():
    database = r"C:\Users\Gerald Post\AppData\Local\Packages\Microsoft.MicrosoftStickyNotes_8wekyb3d8bbwe\LocalState\plum.sqlite"

    # create a database connection
    conn = create_connection(database)
    with conn:
        data = get_sticky_note_text(conn)
        text = re.sub('(\\n)?(\\\\id=)(\d|\w){8}-(\d|\w){4}-(\d|\w){4}-(\d|\w){4}-(\d|\w){12}\s','~', data[0]).split('~')
        for line in text:
            print(line)
        
            
if __name__ == '__main__':
    main()

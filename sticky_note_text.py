import sqlite3
import re
from datetime import datetime, timedelta


# StickyNote class that creates new object to create connection and
# interact with the database that hosts the sticky note information 
class StickyNote:
    def __init__(self, database):
        self._database = database
        self._conn = None
    
    def get_database(self):
        return self._database

    def get_conn(self):
        return self._conn
    
    # Creating a connection with the sqllite database and storing connection in 
    # database member variable 
    def create_connection(self, sticky_db):
        try:
            conn = sqlite3.connect(sticky_db)
        except Error as erorr:
            print(erorr)

        self._conn = conn
    
    # After connection is made, using SELECT statment to access 
    # the desired rows and columns from the db 
    def get_sticky_note_text(self):
        cur = self._conn.cursor()
        cur.execute("SELECT Text FROM Note")
        rows = cur.fetchone()
        return rows


def get_events(text: list) -> dict:
    """Take in the list of string objects from the sticky note database, and
    return a dictionary with dates as keys, and events as associated values."""
    # find which text entries contain dates
    events = {}

    for line in text:
        # format of sticky note events are separated by ':'
        line = line.split(':')

        # check if numeric input to create date object
        if line[0] != '' and line[0][0].isdigit():
            # using datetime to convert dates to datetime objects
            dt = datetime.strptime(line[0], "%m/%d/%Y %H%M")
            end_time = dt + timedelta(hours=2)
            events[dt.strftime('%Y-%m-%dT%H:%M:%S')] = line[1], end_time.strftime('%Y-%m-%dT%H:%M:%S')

    return events


# Main function that creates a StickyNote object and gets a list of the desired text 
def create_sticky():
    # replace with own user name for the path to the sqllite database 
    database = r"C:\Users\YOUR_USER_NAME_HERE\AppData\Local\Packages\Microsoft.MicrosoftStickyNotes_8wekyb3d8bbwe\LocalState\plum.sqlite"

    sticky_note = StickyNote(database)

    # create a database connection
    sticky_note.create_connection(database)

    with sticky_note.get_conn():
        data = sticky_note.get_sticky_note_text()
        # using RE to remove unwanted ID text attached to the strings 
        text = (re.sub('(\\n)?(\\\\id=)(\d|\w){8}-(\d|\w){4}-(\d|\w){4}-(\d|\w){4}-(\d|\w){12}\s', '~', data[0]).split(
            '~'))
        events = get_events(text)

    return events


if __name__ == "__main__":
	# Testing if the events got returned correctly or not, if ran from this module 
    print(create_sticky())

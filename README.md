# Sticky-Note-text-puller
Takes the text from the Windows Sticky Notes desktop app, and stores will take text in a specifc date-time format to create a new Google Calendar event. 

### How to use: 
Follow the instructions for the Google API Quickstart here: [Python Quickstart](https://developers.google.com/calendar/quickstart/python)
<br></br>
Run <code>pip install -r requirements.txt</code> to install all required dependencies 

### Implementation:
The sqlite3 module is used to connect to the database that stores the Sticky Notes data on the user's local Windows machine. When a connection is made, then the text from the Sticky Note is found by executing a SQL SELECT statement, this will return the appropriate rows from the table. 

Since all of the lines of text come with an attached ID number the 're' module is imported to use regular expressions to replace all of the ID's to get an easier list to work with. All events are stored into a dictionary with the start-time as the key, and an associated value that is a tuple storing the event summary and end-time. 

The Google API template provided in the Quickstart is used to check user credentials, and allow the user to interact with the Google Calendar API. Methods are implemented to check if the events from the sticky note currently exist, if not the new events are created. 

### Future Plans: 
Allow the application to take in any date-time formats for the new event. 

Modify the sqllite database to allow for a trigger to run the python script whenever a new insert is made (a new line of text in the Sticky Note). 

Would like to try to import the text from the sticky note to Apple notes on iPhone, but have not found any good documentation on interfacing from Windows to Apple notes via Python. 


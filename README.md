# Sticky-Note-text-puller
Takes the text from the Windows Sticky Notes desktop app, and stores will take text in a specifc date-time format to create a new Google Calendar event. 

### How to use: 
Follow the instruciton for the Google API quickstart here: [a linkl](https://developers.google.com/calendar/quickstart/python)

### Implementation:
The sqlite3 module is used to conect to the database that stores the sticky note data on the user's local Windows machine. When a connection is made, then the text from the sticky note is found by executing a SQL SELECT statement, this will return the appropriate rows from the table. 

Since all of the lines of text come with an attached ID number the 're' module is imported to use regular expressions to replace all of the ID's to get an easier list to work with. 


### Future Plans: 
Allow the application to take in any date-time formats for the new event. 

Would like to try to import the text from the sticky note to Apple notes on iPhone, but have not found any good documentation on interfacing from Windows to Apple notes via Python. 

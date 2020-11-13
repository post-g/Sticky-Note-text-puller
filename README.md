# Sticky-Note-text-puller
Takes the text from the windows sticky note desktop app and stores into a python list for later use. 

### Implementation:
The sqlite3 module is used to conect to the database that stores the sticky note data on the user's local Windows machine. When a connection is made, then the text from the sticky note is found by executing a SQL SELECT statement, this will return the appropriate rows from the table. 

Since all of the lines of text come with an attached ID number the 're' module is imported to use regular expressions to replace all of the ID's to get an easier list to work with. 


### Future Plans: 
Using Google API, take the text that include dates and input the given note into personal Google Calednar. 

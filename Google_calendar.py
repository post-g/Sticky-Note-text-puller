from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import sticky_note_text as snt

# If modifying these scopes, delete the file token.pickle.
# Using the calendar scope to allow read & write access to Calendars
SCOPES = ['https://www.googleapis.com/auth/calendar']


def main():
    """Using provided code from Google API documentation for accessing
       Google Calendar objects.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # get current events 
    curr_events = get_current_events(service)

    # using create event function, then looping through all events
    # to create new events in Google Calendar
    events = create_event()

    for event in events:
        # check if an event already exists
        # if it does, do not create new event in calendar 
        if not check_if_event_exists(curr_events, event):
            event = service.events().insert(calendarId='primary', body=event).execute()
            print(f"Event created: {event['summary']}\nFor Date: {event['start']['dateTime']}\nUse Link To Modify Event: {event.get('htmlLink')}\n")
        else:
            print(f'**{event["summary"]}** already exists in calendar on {event["start"]["dateTime"]}.\n')

def get_current_events(service):
    '''Return 50 of the most current events starting at the beginning of the current month.'''
    # get all events starting at first day of current month 
    first_day_of_month = datetime.datetime.today().replace(day=1).isoformat() + 'Z'
    events_result = service.events().list(calendarId='primary', timeMin=first_day_of_month,
                                               maxResults=50, singleEvents=True,
                                               orderBy='startTime').execute()

    return events_result.get('items', [])


def check_if_event_exists(curr_events, event_to_add):
    '''Given an event, check if that event exists in the current Google Calendar.'''
    
    # creating a list of event summary and using .split('T') to only get YYYY-MM-DD without start-end time
    current_events = [(event['summary'], event['start']['dateTime'].split('T')[0]) for event in curr_events] 
    
    # loop thru events to see if our new event has already been created 
    for summary, date in current_events:
        if summary == event_to_add['summary'] and date == event_to_add['start']['dateTime'].split('T')[0]:
            return True

    return False
   

def create_event():
    """Takes a dictionary of events from the sticky note text puller,
    and returns a list of events to create new Google Calendar events."""
    sticky_note_events = snt.create_sticky()
    events = []
    for date, values in sticky_note_events.items():
        event = {
            'summary': values[0],
            'start': {
                'dateTime': date,
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': values[1],
                'timeZone': 'America/Los_Angeles',
            },
            'recurrence': [
                'RRULE:FREQ=DAILY;COUNT=1'
            ],
            'reminders': {
                'useDefault': True
            },
        }
        events.append(event)

    return events


if __name__ == '__main__':
    main()

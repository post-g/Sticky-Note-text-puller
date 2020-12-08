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

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    events = create_event()
    for event in events:
        event = service.events().insert(calendarId='primary', body=event).execute()
        print('Event created: %s' % (event.get('htmlLink')))


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

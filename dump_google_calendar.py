from __future__ import print_function
import datetime
from dateutil.relativedelta import relativedelta
import json
import os.path
import sys
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def main(args):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    min_date = datetime.datetime(int(args[1]), 1, 1, 0, 0, 0)
    min_str = min_date.isoformat() + 'Z'
    max_str = (min_date + relativedelta(years=1) - datetime.timedelta(seconds=1)).isoformat() + 'Z'
    events_result = service.events().list(calendarId='primary', timeMin=min_str, timeMax=max_str,
                                        maxResults=1000, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    # # print(json.dumps(events))
    print(json.dumps(list(map(lambda e: {
        'summary': e.get('summary'),
        'start': e.get('start').get('dateTime'),
        'end': e.get('end').get('dateTime'),
        'location': e.get('location'),
        'description': e.get('description')}, events))))

if __name__ == '__main__':
    args = sys.argv

    if len(args) != 2:
        print('Usage: python dump_google_calendar.py <year>')
        sys.exit(1)

    main(args)

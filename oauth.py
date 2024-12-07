from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from tutoring.models import GoogleCredentials
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

CREDENTIALS_FILE = 'client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/calendar.events']

def get_google_credentials():
    try:
        creds = GoogleCredentials.objects.first()
        if creds:
            return Credentials(
                token=creds.token,
                refresh_token=creds.refresh_token,
                token_uri=creds.token_uri,
                client_id=creds.client_id,
                client_secret=creds.client_secret,
                scopes=creds.scopes.split(',')
            )
    except GoogleCredentials.DoesNotExist:
        return None

def save_google_credentials(credentials):
    GoogleCredentials.objects.update_or_create(
        id=1,
        defaults={
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': ','.join(credentials.scopes)
        }
    )

def get_authenticated_service():
    credentials = get_google_credentials()
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            credentials = flow.run_local_server(port=8080)
        save_google_credentials(credentials)

    service = build('calendar', 'v3', credentials=credentials)
    return service

def create_google_meet_link():
    service = get_authenticated_service()
    event = {
        'summary': 'Google Meet',
        'description': 'A Google Meet event',
        'start': {
            'dateTime': '2023-10-10T10:00:00-07:00',
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': '2023-10-10T10:30:00-07:00',
            'timeZone': 'America/Los_Angeles',
        },
        'conferenceData': {
            'createRequest': {
                'requestId': 'sample123',
                'conferenceSolutionKey': {
                    'type': 'hangoutsMeet'
                }
            }
        },
        'attendees': [
            {'email': 'attendee@example.com'},
        ],
    }

    event = service.events().insert(calendarId='primary', body=event, conferenceDataVersion=1).execute()
    return event.get('hangoutLink')
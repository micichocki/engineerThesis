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

def get_authenticated_service(user):
    google_creds = GoogleCredentials.objects.get(user=user)
    credentials = Credentials(
        token=google_creds.token,
        refresh_token=google_creds.refresh_token,
        token_uri=google_creds.token_uri,
        client_id=google_creds.client_id,
        client_secret=google_creds.client_secret,
        scopes=['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/calendar.events']
    )
    service = build('calendar', 'v3', credentials=credentials)
    return service

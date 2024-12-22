from googleapiclient.discovery import build
from tutoring.models import GoogleCredentials
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

CREDENTIALS_FILE = 'client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/calendar.events']

def get_google_credentials(user):
    try:
        google_creds = GoogleCredentials.objects.get(user=user)
        credentials = Credentials(
            token=google_creds.token,
            refresh_token=google_creds.refresh_token,
            token_uri=google_creds.token_uri,
            client_id=google_creds.client_id,
            client_secret=google_creds.client_secret,
            scopes=google_creds.scopes.split(','),
        )

        if not credentials.valid and credentials.refresh_token:
            credentials.refresh(Request())
            GoogleCredentials.objects.filter(user=user).update(
                token=credentials.token
            )

        return credentials
    except GoogleCredentials.DoesNotExist:
        return None

def get_authenticated_service(user):
    credentials = get_google_credentials(user)
    if credentials:
        return build('calendar', 'v3', credentials=credentials)
    raise ValueError("Google credentials not found for the user.")
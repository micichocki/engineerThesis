from google_auth_oauthlib.flow import InstalledAppFlow
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken

from engineerThesis.serializers import RegisterSerializer
from oauth import CREDENTIALS_FILE, SCOPES, get_authenticated_service
from tutoring.exceptions.exceptions import DuplicateKeyException
from tutoring.models import GoogleCredentials, Lesson


class TokenVerifyView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        token = request.data.get('token')
        try:
            UntypedToken(token)
            return Response({"isValid": True}, status=status.HTTP_200_OK)
        except (InvalidToken, TokenError) as e:
            return Response({"isValid": False,"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
        except DuplicateKeyException as e:
            return Response({"error": e.message}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)


class AuthorizeGoogleCalendarView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
        auth_url, _ = flow.authorization_url(prompt='consent')
        return Response({'auth_url': auth_url})


class GoogleCalendarCallbackView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES, redirect_uri='http://localhost:3000/pending-lessons/')
        flow.fetch_token(authorization_response=request.build_absolute_uri())

        credentials = flow.credentials
        GoogleCredentials.objects.update_or_create(
            user=request.user,
            defaults={
                'token': credentials.token,
                'refresh_token': credentials.refresh_token,
                'token_uri': credentials.token_uri,
                'client_id': credentials.client_id,
                'client_secret': credentials.client_secret,
                'scopes': credentials.scopes
            }
        )

        return Response({"message": "Google Calendar authorization successful"}, status=status.HTTP_200_OK)

class CreateGoogleMeetView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, lesson_id, *args, **kwargs):
        try:
            lesson = Lesson.objects.get(id=lesson_id)
        except Lesson.DoesNotExist:
            return Response({"error": "Lesson not found"}, status=status.HTTP_404_NOT_FOUND)
        service = get_authenticated_service()
        event = {
            'summary': lesson.description,
            'description': lesson.description,
            'start': {
                'dateTime': lesson.start_time.isoformat(),
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': lesson.end_time.isoformat(),
                'timeZone': 'UTC',
            },
            'conferenceData': {
                'createRequest': {
                    'requestId': f'lesson-{lesson.id}',
                    'conferenceSolutionKey': {
                        'type': 'hangoutsMeet'
                    }
                }
            },
            'attendees': [
                {'email': lesson.student.user.email},
                {'email': lesson.tutor.user.email}
            ],
        }

        event = service.events().insert(calendarId='primary', body=event, conferenceDataVersion=1).execute()
        lesson.google_meet_url = event.get('hangoutLink')
        lesson.save()

        return Response({"google_meet_link": lesson.google_meet_url}, status=status.HTTP_200_OK)

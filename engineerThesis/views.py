from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken

from engineerThesis.serializers import RegisterSerializer
from tutoring.exceptions.exceptions import DuplicateKeyException


class TokenVerifyView(APIView):
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

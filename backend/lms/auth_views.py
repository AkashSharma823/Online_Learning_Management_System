from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        identifier = (request.data.get("username") or request.data.get("email") or "").strip()
        password = request.data.get("password") or ""

        if not identifier or not password:
            return Response({"detail": "Username/email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=identifier, password=password)
        if not user:
            candidate = User.objects.filter(email__iexact=identifier).first()
            if candidate:
                user = authenticate(request, username=candidate.username, password=password)

        if not user:
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": UserSerializer(user).data,
        })

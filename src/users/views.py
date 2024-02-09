from .models import User
from .serializers import UserSerializer
# from django.contrib.auth import authenticate
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

from .authentication import CustomUserAuthenticationBackend


class UserSignUpView(generics.CreateAPIView):
    """
    This endpoint allows a user to sign up.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]



class UserLoginView(APIView):
    """
    This endpoint allows a user to login.
    """
    permission_classes = [permissions.AllowAny]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def post(self, request, *args, **kwargs):
        
        email_or_phone = request.data.get("email_or_phone",)
        password = request.data.get("password",)

        if email_or_phone is None or password is None:
            return Response({'error': 'Please provide both email/phone and password'}, status=status.HTTP_400_BAD_REQUEST)    

        user = CustomUserAuthenticationBackend().authenticate(request, username=email_or_phone, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })
        return Response("Invalid Credentials", status=status.HTTP_400_BAD_REQUEST)
    


class UserLogoutView(APIView):
    """
    This endpoint allows a user to logout.
    """
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class BlacklistTokenView(APIView):
    """
    This endpoint allows a user to blacklist a token.
    """
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.response import Response
from rest_framework import status

from rest_framework.views import APIView

from . import serializers
from .models import Customer, CustomerProfile


from users.authentication import CustomUserAuthenticationBackend
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework_simplejwt.authentication import JWTAuthentication

from users.customJWT import CustomJWTAuthenticationClass

from rest_framework_simplejwt.views import TokenRefreshView



class CustomerSignupView(APIView):
    """
    This endpoint allows a CUSTOMER to signup.
    """
    permission_classes = [permissions.AllowAny]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def post(self, request, *args, **kwargs):
        serializer = serializers.CustomerSerializer(data=request.data)
        if serializer.is_valid():
            customer = serializer.save()
            if customer:
                return Response({
                    'user': serializers.CustomerSerializer(customer).data
                },
                status=status.HTTP_201_CREATED
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CustomerLoginView(APIView):

    """
    This endpoint allows a customer to login.
    """
    permission_classes = [permissions.AllowAny]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def post(self, request, *args, **kwargs):
        
        email_or_phone = request.data.get("email_or_phone",)
        password = request.data.get("password",)

        if email_or_phone is None or password is None:
            return Response({'error': 'Please provide both email/phone and password'}, status=status.HTTP_400_BAD_REQUEST)    

        customer = CustomUserAuthenticationBackend().authenticate(request, username=email_or_phone, password=password)

        if customer and customer.role == Customer.Role.CUSTOMER:
            refresh = RefreshToken.for_user(customer)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': serializers.CustomerProfileSerializer(customer).data
            },
            status=status.HTTP_200_OK
            )
        return Response("Invalid Credentials", status=status.HTTP_400_BAD_REQUEST)
    



class CustomerProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows CUSTOMER profiles to be viewed or edited.
    """
    queryset = CustomerProfile.objects.all()
    serializer_class = serializers.CustomerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    authentication_classes = [JWTAuthentication,]

    def get_queryset(self):
        return CustomerProfile.objects.filter(customer=self.request.user)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

    def patch(self, request, *args, **kwargs):
        bio = request.data.get("bio", None)
        image = request.data.get("image", None)
        full_name = request.data.get("full_name", None)
        phone_number = request.data.get("phone_number", None)
        
        if full_name:
            object_ = self.get_object()
            object_.customer.full_name = full_name
            object_.customer.save()
            return Response(serializers.CustomerProfileSerializer(object_).data)
        if phone_number:
            object_ = self.get_object()
            object_.customer.phone_number = phone_number
            object_.customer.save()
            return Response(serializers.CustomerProfileSerializer(object_).data)

        if bio:
            customer = self.get_object()
            customer.bio = bio
            customer.save()
            return Response(
                serializers.CustomerProfileSerializer(customer).data,
                status=status.HTTP_200_OK
                
            )
        if image:
            customer = self.get_object()
            customer.image = image
            customer.save()
            return Response(
                serializers.CustomerProfileSerializer(customer).data,
                status=status.HTTP_200_OK
            )

        else:
            return super().partial_update(request, *args, **kwargs)
    


class CustomerLogOutView(APIView):
    """
    This endpoint allows a user to logout.
    """
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication,]

    def post(self, request, *args, **kwargs):
        try:
            # Handle blacklisting and logout using access_token and custom JWT authentication class with redis
            access_token = request.headers.get("Authorization").split(" ")[1]
            CustomJWTAuthenticationClass().blacklist_token(access_token)
            return Response(status=status.HTTP_205_RESET_CONTENT, data={"message": "Logged out successfully"})            
        except Exception as e:
            return Response({'error': str(e)}, status=400)



class CustomerTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get("refresh",)
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
                new_access_token = token.access_token
                return Response(
                    {
                    'access': str(new_access_token),
                    },
                    status=status.HTTP_200_OK
                )
        except Exception as e:
            return Response({'error': str(e)}, status=400)
        return Response({'error': 'Invalid token'}, status=400)
    

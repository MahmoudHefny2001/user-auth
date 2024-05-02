from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.response import Response
from rest_framework import status

from rest_framework.views import APIView

from . import serializers
from .models import Customer, CustomerProfile


from apps.users.authentication import CustomUserAuthenticationBackend
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.users.customJWT import CustomJWTAuthenticationClass

from rest_framework_simplejwt.views import TokenRefreshView


import jwt

from django.conf import settings

from .mail import send_reset_password_email


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
        return Response(
            {
            "error": "Invalid Credentials", 
            }, 
            status=status.HTTP_400_BAD_REQUEST
        )
    



class CustomerProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows CUSTOMER profiles to be viewed or edited.
    """
    queryset = CustomerProfile.objects.all()
    serializer_class = serializers.CustomerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    authentication_classes = [JWTAuthentication,]

    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        if self.request.user.is_superuser:
            return CustomerProfile.objects.all()
         
        return CustomerProfile.objects.filter(customer=self.request.user)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

    
    def partial_update(self, request, *args, **kwargs):
        bio = request.data.get("bio", None)
        image = request.data.get("image", None)
        full_name = request.data.get("full_name", None)
        phone_number = request.data.get("phone_number", None)
        email = request.data.get("email", None)
        address = request.data.get("address", None)

        if bio or image or full_name or phone_number or email or address:
            instance = self.get_object()
            customer = instance.customer
            if address:
                customer.address = address
            if bio:
                instance.bio = bio
            if image:
                instance.image = image
            if full_name:
                instance.customer.full_name = full_name
            if email:
                instance.customer.email = email
            if phone_number:
                instance.customer.phone_number = phone_number
            instance.customer.save()
            instance.save()
            return Response(serializers.CustomerProfileSerializer(instance).data)
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
    


import threading

class CustomerPasswordResetView(APIView):

    permission_classes = [permissions.AllowAny,]
    # permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = [JWTAuthentication,]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')   
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            customer = Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            return Response({'error': 'User not found with this email'}, status=status.HTTP_404_NOT_FOUND)
        
        # Generate JWT token
        token = jwt.encode({'user_id': customer.pk}, settings.SECRET_KEY, algorithm='HS256')
        
        # Send the email without blocking the response using a new thread
        threading.Thread(target=send_reset_password_email, args=(email, token)).start()
        
        return Response({'success': 'Password reset token sent'}, status=status.HTTP_200_OK)
        


class CustomerPasswordUpdateMailView(APIView):

    permission_classes = [permissions.AllowAny,]
    # permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = [JWTAuthentication,]

    def post(self, request, *args, **kwargs):
        token = request.data.get('token')
        new_password = request.data.get('new_password')

        if not token or not new_password:
            return Response({'error': 'Token and new password are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = decoded_token.get('user_id')
            user = Customer.objects.get(pk=user_id)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token has expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.DecodeError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        except Customer.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Update password
        user.set_password(new_password)
        user.save()
        return Response({'success': 'Password updated successfully'}, status=status.HTTP_200_OK)




class CustomerPasswordUpdateView(APIView):

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication,]

    def post(self, request, *args, **kwargs):
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not old_password or not new_password:
            return Response({'error': 'Old password and new password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user

        if not user.check_password(old_password):
            return Response({'error': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({'success': 'Password updated successfully'}, status=status.HTTP_200_OK)
    


class CustomerDeleteView(APIView):
    
        permission_classes = [permissions.IsAuthenticated]
        authentication_classes = [JWTAuthentication,]
    
        def delete(self, request, *args, **kwargs):
            user = request.user
            user.delete()
            return Response({'success': 'Account deleted successfully'}, status=status.HTTP_200_OK)



# from rest_framework import generics
# from allauth.socialaccount.providers.oauth2.views import OAuth2Adapter, OAuth2LoginView
# from allauth.socialaccount.app_settings import QUERY_PARAMETER_CONNECT_OR_LOGIN
# from allauth.socialaccount.models import SocialAccount, SocialToken


# class CustomOAuth2Adapter(OAuth2Adapter):
#     provider_id = 'google'  # or 'facebook'

#     def get_provider_url(self, request):
#         return f'/{self.provider_id}/login/'

# class CustomOAuth2LoginView(OAuth2LoginView):
#     adapter_class = CustomOAuth2Adapter

# class GoogleSocialLoginView(generics.CreateAPIView):
#     serializer_class = serializers.CustomerSerializer

#     def create(self, request, *args, **kwargs):
#         next_url = request.query_params.get('next', '/')
#         login_url = f'/{self.request.auth.provider}/login/?{QUERY_PARAMETER_CONNECT_OR_LOGIN}=1&next={next_url}'
#         return Response({'login_url': login_url})

# class GoogleSocialSignupView(generics.CreateAPIView):
#     serializer_class = serializers.CustomerSerializer

#     def create(self, request, *args, **kwargs):
#         adapter = CustomOAuth2Adapter()
#         request.user.social_account.set_provider(adapter.get_provider())
#         request.user.social_account.extra_data['access_token'] = request.data['access_token']
#         request.user.social_account.extra_data['token_type'] = request.data['token_type']
#         token = SocialToken(app=adapter.get_provider(), token=request.data['access_token'], token_type=request.data['token_type'])
#         token.save()



# class CustomerEmailVerificationView(APIView):
#     permission_classes = [permissions.IsAuthenticated]
#     authentication_classes = [JWTAuthentication,]

#     def post(self, request, *args, **kwargs):
#         try:
#             customer = Customer.objects.get(pk=request.user.pk)
#             profile = CustomerProfile.objects.get(customer=customer)
#             if profile.is_verified:
#                 return Response({'error': 'Email is already verified'}, status=400)
            
#             profile.is_verified = True
#             profile.save()

#             return Response({'success': 'Email verified successfully'}, status=200)
#         except Customer.DoesNotExist:
#             return Response({'error': 'User not found'}, status=404)

#         except Exception as e:
#             return Response({'error': str(e)}, status=400)
        
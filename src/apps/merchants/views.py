from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.response import Response
from rest_framework import status

from rest_framework.views import APIView

from . import serializers
from .models import Merchant, MerchantProfile

from rest_framework_simplejwt.views import TokenRefreshView

from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.users.customJWT import CustomJWTAuthenticationClass
from apps.users.authentication import CustomUserAuthenticationBackend


import jwt
from django.conf import settings


class MerchantSignupView(APIView):
    """
    This endpoint allows a MERCHANT to signup.
    """
    permission_classes = [permissions.AllowAny]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def post(self, request, *args, **kwargs):
        request.data["full_name"] = request.data["business_name"]
        try:
            serializer = serializers.MerchantSerializer(
                data=request.data
            )
            if serializer.is_valid():
                merchant = serializer.save()
                if merchant:
                    return Response({
                        'merchant': serializers.MerchantSerializer(merchant).data
                    },
                    status=status.HTTP_201_CREATED
                    )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                "error": str(e)
            },
            status=status.HTTP_400_BAD_REQUEST
            )
        

    
class MerchantLoginView(APIView):

    """
    This endpoint allows a merchant to login.
    """
    permission_classes = [permissions.AllowAny]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def post(self, request, *args, **kwargs):
        
        email_or_phone = request.data.get("email_or_phone",)
        password = request.data.get("password",)

        if email_or_phone is None or password is None:
            return Response({'error': 'Please provide both email/phone and password'}, status=status.HTTP_400_BAD_REQUEST)    

        merchant = CustomUserAuthenticationBackend().authenticate(request, username=email_or_phone, password=password)

        if merchant and merchant.role == Merchant.Role.MERCHANT:
            refresh = RefreshToken.for_user(merchant)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'merchant': serializers.MerchantSerializer(merchant).data
            },
            status=status.HTTP_200_OK
            )
        return Response("Invalid Credentials", status=status.HTTP_400_BAD_REQUEST)



class MerchantProfileViewSet(viewsets.ModelViewSet):
    queryset = MerchantProfile.objects.all()
    serializer_class = serializers.MerchantProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [CustomJWTAuthenticationClass, JWTAuthentication]

    http_method_names = ["get", "put", "patch", "delete",]

    def get_queryset(self):
        return MerchantProfile.objects.filter(merchant=self.request.user)
    

    def perform_create(self, serializer):
        serializer.save(merchant=self.request.user)


    def partial_update(self, request, *args, **kwargs):

        """
            partial merchant update
            allow update only one or more of the fields
        """

        try:
            
            # merchant_data
            address = request.data.get("address", None)
            payment_information = request.data.get("payment_information", None)
            terms_agreement = request.data.get("terms_agreement", None)
            email = request.data.get("email", None)
            business_name = request.data.get("business_name", None)
            phone_number = request.data.get("phone_number", None)
            

            # merchant_profile_data
            image = request.data.get("image", None)
            merchant_zip_code = request.data.get("merchant_zip_code", None)
            tax_id = request.data.get("tax_id", None)
            logo = request.data.get("logo", None)
            shipping_address = request.data.get("shipping_address", None)
            shipping_options = request.data.get("shipping_options", None)
            website_url = request.data.get("website_url", None)
            facebook_url = request.data.get("facebook_url", None)
            twitter_url = request.data.get("twitter_url", None)
            instagram_url = request.data.get("instagram_url", None)
            linkedin_url = request.data.get("linkedin_url", None)
            about_us = request.data.get("about_us", None)
            return_policy = request.data.get("return_policy", None)

            
            merchant_profile = self.get_object()
            
            # update merchant data
            if address:
                merchant_profile.merchant.address = address
            if payment_information:
                merchant_profile.merchant.payment_information = payment_information
            if terms_agreement:
                merchant_profile.merchant.terms_agreement = terms_agreement
            if email:
                merchant_profile.merchant.email = email
            if business_name:
                merchant_profile.merchant.full_name = business_name
            if phone_number:
                merchant_profile.merchant.phone_number = phone_number
            
            merchant_profile.merchant.save()

            # update merchant profile data
            if image:
                merchant_profile.image = image
            if merchant_zip_code:
                merchant_profile.merchant_zip_code = merchant_zip_code
            if tax_id:
                merchant_profile.tax_id = tax_id
            if logo:
                merchant_profile.logo = logo
            if shipping_address:
                merchant_profile.shipping_address = shipping_address
            if shipping_options:
                merchant_profile.shipping_options = shipping_options
            if website_url:
                merchant_profile.website_url = website_url
            if facebook_url:
                merchant_profile.facebook_url = facebook_url
            if twitter_url:
                merchant_profile.twitter_url = twitter_url
            if instagram_url:
                merchant_profile.instagram_url = instagram_url
            if linkedin_url:
                merchant_profile.linkedin_url = linkedin_url
            if about_us:
                merchant_profile.about_us = about_us
            if return_policy:
                merchant_profile.return_policy = return_policy
            
            merchant_profile.save()

            return Response(
                {
                    'merchant': serializers.MerchantProfileSerializer(merchant_profile).data
                },
                status=status.HTTP_200_OK
            )
    

        except Exception as e:
            return Response({'error': str(e)}, status=400)





class MerchantLogOutView(APIView):
    """
    This endpoint allows a Merchant to logout.
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




class MerchantTokenRefreshView(TokenRefreshView):
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

from .mail import send_reset_password_email

class MerchantPasswordResetMailView(APIView):

    permission_classes = [permissions.AllowAny,]
    # permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = [JWTAuthentication,]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')   
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            merchant = Merchant.objects.get(email=email)
        except Merchant.DoesNotExist:
            return Response({'error': 'User not found with this email'}, status=status.HTTP_404_NOT_FOUND)
        
        # Generate JWT token
        token = jwt.encode({'user_id': merchant.pk}, settings.SECRET_KEY, algorithm='HS256')
        
        # Send the email without blocking the response using a new thread
        threading.Thread(target=send_reset_password_email, args=(email, token)).start()
        
        return Response({'success': 'Password reset token sent'}, status=status.HTTP_200_OK)
        


class MerchantPasswordUpdateMailView(APIView):

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
            user = Merchant.objects.get(pk=user_id)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token has expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.DecodeError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        except Merchant.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Update password
        user.set_password(new_password)
        user.save()
        return Response({'success': 'Password updated successfully'}, status=status.HTTP_200_OK)




class MerchantPasswordUpdateView(APIView):

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
    


class MerchantDeleteView(APIView):
    
        permission_classes = [permissions.IsAuthenticated]
        authentication_classes = [JWTAuthentication,]
    
        def delete(self, request, *args, **kwargs):
            user = request.user
            user.delete()
            return Response({'success': 'Account deleted successfully'}, status=status.HTTP_200_OK)
        

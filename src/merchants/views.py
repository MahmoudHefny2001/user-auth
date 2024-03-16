from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.response import Response
from rest_framework import status

from rest_framework.views import APIView

from . import serializers
from .models import Merchant, MerchantProfile


from users.authentication import CustomUserAuthenticationBackend
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework_simplejwt.authentication import JWTAuthentication

from users.customJWT import CustomJWTAuthenticationClass

from rest_framework_simplejwt.views import TokenRefreshView


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
        
        try:
            merchant = self.get_object()

            if "merchant" in request.data:
                
                """
                partial merchant update
                allow update only one or more of the fields
                """

                if "email" in request.data["merchant"]:
                    merchant.merchant.email = request.data["merchant"]["email"]
                    merchant.merchant.save()
                    return Response(serializers.MerchantProfileSerializer(merchant).data)
                if "phone_number" in request.data["merchant"]:
                    merchant.merchant.phone_number = request.data["merchant"]["phone_number"]
                    merchant.merchant.save()
                    return Response(serializers.MerchantProfileSerializer(merchant).data)
                if "address" in request.data["merchant"]:
                    merchant.merchant.address = request.data["merchant"]["address"]
                    merchant.merchant.save()
                    return Response(serializers.MerchantProfileSerializer(merchant).data)
                if "payment_information" in request.data["merchant"]:
                    merchant.merchant.payment_information = request.data["merchant"]["payment_information"]
                    merchant.merchant.save()
                    return Response(serializers.MerchantProfileSerializer(merchant).data)
                if "terms_agreement" in request.data["merchant"]:
                    merchant.merchant.terms_agreement = request.data["merchant"]["terms_agreement"]
                    merchant.merchant.save()
                    return Response(serializers.MerchantProfileSerializer(merchant).data)
                if "business_name" in request.data["merchant"]:
                    merchant.merchant.full_name = request.data["merchant"]["business_name"]
                    merchant.merchant.save()
                    return Response(serializers.MerchantProfileSerializer(merchant).data)
            if "about_us" in request.data:
                merchant.about_us = request.data["about_us"]
                merchant.save()
                return Response(serializers.MerchantProfileSerializer(merchant).data)

            if "website_url" in request.data:
                merchant.website_url = request.data["website_url"]
                merchant.save()
                return Response(serializers.MerchantProfileSerializer(merchant).data)
            
            if "facebook_url" in request.data:
                merchant.facebook_url = request.data["facebook_url"]
                merchant.save()
                return Response(serializers.MerchantProfileSerializer(merchant).data)
            
            if "linkedin_url" in request.data:
                merchant.linkedin_url = request.data["linkedin_url"]
                merchant.save()
                return Response(serializers.MerchantProfileSerializer(merchant).data)
            
            if "instagram_url" in request.data:
                merchant.instagram_url = request.data["instagram_url"]
                merchant.save()
                return Response(serializers.MerchantProfileSerializer(merchant).data)
            
            else:
                return super().partial_update(request, *args, **kwargs)
            

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
    

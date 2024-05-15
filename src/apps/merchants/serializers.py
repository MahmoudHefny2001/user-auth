from rest_framework import serializers

from .models import Merchant, MerchantProfile


class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = [
            "id",
            "email",
            "phone_number",
            "full_name",
            "address",
            "payment_information",
            "terms_agreement",
            "password",
        ]
        
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        try:
            email = validated_data.get("email")
            phone_number = validated_data.get("phone_number")
            password = validated_data.get("password")
            business_name = validated_data.get("full_name")
            
            address = validated_data.get("address", None)
            payment_information = validated_data.get("payment_information", None)
            terms_agreement = validated_data.get("terms_agreement", None)

            if email is None or phone_number is None or password is None or business_name is None:
                raise serializers.ValidationError("Please provide all required fields.")
            
            merchant = Merchant.objects.create_merchant(**validated_data)
            return merchant
        except Exception as e:
            raise serializers.ValidationError(str(e))
    
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["business_name"] = representation["full_name"]
        del representation["full_name"]
        return representation
    




class MerchantProfileSerializer(serializers.ModelSerializer):
    merchant = MerchantSerializer(read_only=True)
    class Meta:
        model = MerchantProfile
        fields = [
            "id",
            "logo",
            "image", 
            "tax_id",
            "merchant",
            "about_us",
            "twitter_url",
            "website_url",
            "facebook_url",
            "linkedin_url",
            "return_policy",
            "instagram_url",
            "shipping_address",
            "shipping_options",
            "merchant_zip_code", 
        ]
    



class MerchantSerializerForCustomers(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = [
            "full_name",
            "address",
            "payment_information",
            "terms_agreement",
        ]
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["business_name"] = representation["full_name"]
        del representation["full_name"]
        return representation


class MerchantProfileSerializerForCustomers(serializers.ModelSerializer):
    merchant = MerchantSerializerForCustomers(read_only=True)
    class Meta:
        model = MerchantProfile
        fields = [
            "id",
            "logo",
            "image", 
            "tax_id",
            "merchant",
            "about_us",
            "twitter_url",
            "website_url",
            "facebook_url",
            "linkedin_url",
            "return_policy",
            "instagram_url",
            "shipping_address",
            "shipping_options",
            "merchant_zip_code", 
        ]
        

from rest_framework import serializers
from .models import Customer, CustomerProfile


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "id", "email", 
            # "username", 
            "full_name", "phone_number", "password"
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        try:
            email = validated_data.get("email")
            phone_number = validated_data.get("phone_number")
            password = validated_data.get("password")
            full_name = validated_data.get("full_name")
            if email is None or phone_number is None or password is None or full_name is None:
                raise serializers.ValidationError("Please provide all required fields.")
            customer = Customer.objects.create_user(**validated_data)
            return customer
        except Exception as e:
            raise serializers.ValidationError(str(e))


class CustomerProfileSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    class Meta:
        model = CustomerProfile
        fields = [
            "id", "customer", "bio", "image"
        ]
        
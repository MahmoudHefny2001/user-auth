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
        customer = Customer.objects.create_user(**validated_data)
        return customer
    


class CustomerProfileSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    class Meta:
        model = CustomerProfile
        fields = [
            "id", "customer", "bio", "image"
        ]
        
from rest_framework.serializers import ModelSerializer

from .models import ContactForm



class ConactFormSerializer(ModelSerializer):
    class Meta:
        model = ContactForm
        fields = ("name", "email", "phone_number", "message", 'created',)
        read_only_fields = ('created',)
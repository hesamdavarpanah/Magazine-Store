from rest_framework.serializers import ModelSerializer
from .models import ContactUs


class ContactUsSerializer(ModelSerializer):
    class Meta:
        model = ContactUs
        fields = "__all__"

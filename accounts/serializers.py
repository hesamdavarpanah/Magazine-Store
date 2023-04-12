from rest_framework.serializers import ModelSerializer
from .models import User, Transaction


class TransactionSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "last_login", "username", "first_name", "last_name", "email", "date_joined", "address",
                  "phone_number", "birth_date", "bio", "credit", "purchased_magazine", "point", "profile_picture"]

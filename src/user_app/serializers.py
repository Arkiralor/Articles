from rest_framework.serializers import ModelSerializer

from user_app.models import UserAccount, UserOTP


class UserAccountSerializer(ModelSerializer):

    class Meta:
        model = UserAccount
        fields = '__all__'


class UserGeneralSerializer(ModelSerializer):

    class Meta:
        model = UserAccount
        fields = (
            "id",
            "username",
            "first_name",
            "middle_name",
            "last_name",
            "email"
        )
        extra_kwargs = {
            "id": {
                "read_only": True
            },
            "username": {
                "read_only": True
            },
            "first_name": {
                "read_only": True
            },
            "middle_name": {
                "read_only": True
            },
            "last_name": {
                "read_only": True
            },
            "email": {
                "read_only": True
            }
        }


class UserRegisterSerializer(ModelSerializer):
    """
    Serializer for User model when an admin is viewing.
    """
    class Meta:
        model = UserAccount
        fields = "__all__"
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }


class UserOTPInputSerializer(ModelSerializer):

    class Meta:
        model = UserOTP
        fields = '__all__'


class UserOTPOutputSerializer(ModelSerializer):
    user = UserGeneralSerializer()

    class Meta:
        model = UserOTP
        fields = '__all__'

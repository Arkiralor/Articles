import re
from typing import Tuple

from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone

from rest_framework_simplejwt.tokens import RefreshToken

from core.boilerplate.abstract_models import TemplateModelUtils
from core.settings import ITEMS_PER_PAGE
from user_app.constants import UserRegex
from user_app.models import UserAccount
from user_app.model_choices import UserAccountChoice
from user_app.serializers import UserAccountSerializer, UserRegisterSerializer, UserGeneralSerializer

from user_app import logger


class UserAccountHelpers(TemplateModelUtils):
    model = UserAccount
    comp_serializer = UserAccountSerializer
    io_serializer = UserRegisterSerializer
    op_serializer = UserGeneralSerializer
    ip_serializer = None

    ALLOWED_PUT_FIELDS = (
        "username",
        "first_name",
        "middle_name",
        "last_name"
    )

    GET_PARAM_CHOICES = (
        "id",
        "username",
        "email",
        "mobile",
        "slug"
    )

    @classmethod
    def search_instances(cls, identifier: str = None, page:int=1):
        qryset = cls.model.objects.filter(
            Q(username__icontains=identifier)
            | Q(first_name__icontains=identifier)
            | Q(middle_name__icontains=identifier)
            | Q(last_name__icontains=identifier)
            | Q(email__icontains=identifier)
            | Q(mobile__icontains=identifier)
            | Q(slug__icontains=identifier)
        ).distinct().order_by("email")

        paginated = Paginator(qryset, ITEMS_PER_PAGE).get_page(page)
        serialized = cls.op_serializer(paginated, many=True).data
        return serialized

    @classmethod
    def get_instance(cls, identifier: str = None, param: str = None, *args, **kwargs) -> Tuple[UserAccount, dict]:
        """
        Finds a single user object based on any one of the unique values, listed as `param`.

        param:
            id | username | email | mobile | slug        
        """
        if param not in cls.GET_PARAM_CHOICES:
            return None, None

        if param is cls.GET_PARAM_CHOICES[0]:
            user = cls.model.objects.filter(pk=identifier).first()
        elif param is cls.GET_PARAM_CHOICES[1]:
            user = cls.model.objects.filter(username=identifier).first()
        elif param is cls.GET_PARAM_CHOICES[2]:
            user = cls.model.objects.filter(email=identifier).first()
        elif param is cls.GET_PARAM_CHOICES[3]:
            user = cls.model.objects.filter(mobile=identifier).first()
        elif param is cls.GET_PARAM_CHOICES[4]:
            user = cls.model.objects.filter(slug=identifier).first()

        serialized = cls.op_serializer(user).data

        return user, serialized

    @classmethod
    def create_jwt_token(cls, user: UserAccount = None):
        tokens = RefreshToken.for_user(user=user)
        resp = {
            'refresh_token': str(tokens),
            'access_token': str(tokens.access_token),
        }
        return resp

    @classmethod
    def create_instance(cls, data: dict = None, user_type: str = None):
        resp = {
            "error": None,
            "instance": None,
            "message": None
        }

        if not data.get("username") or not data.get("email") or not data.get("mobile") or not data.get('password'):
            resp['error'] = "Invalid Data"
            resp['message'] = "'username', 'email', 'mobile' and 'password' are mandatory fields."
            return resp

        if data.get("username") == "" or data.get("email") == "" or data.get("mobile") == "" or data.get('password') == "":
            resp['error'] = "Invalid Data"
            resp['message'] = "'username', 'email', 'mobile' and 'password' are mandatory fields."
            return resp

        if user_type is UserAccountChoice.admin:
            data['is_superuser'] = True
        elif user_type is UserAccountChoice.staff:
            data['is_staff'] = True

        if 'is_superuser' in data.keys() and not user_type == UserAccountChoice.admin:
            del data['is_superuser']

        if 'is_staff' in data.keys() and not user_type == UserAccountChoice.staff:
            del data['is_staff']

        if not re.search(UserRegex.PASSWORD_REGEX, data.get("password")):
            resp['error'] = "Invalid Password"
            resp['message'] = f"Password must be between 8 and 16 characters long, have at least 1 UC, 1 LC , 1 Digital and 1 Special character."
            return resp

        data['password'] = make_password(password=data.get('password', None))

        deserialized = cls.io_serializer(data=data)

        is_valid = deserialized.is_valid()

        if not is_valid:
            resp['error'] = "Serializer Invalid"
            resp['message'] = f"{deserialized.errors}."
            return resp

        deserialized.save()
        resp['message'] = f"User {deserialized.data.get('email')} created successfully."
        resp['instance'] = deserialized.instance

        return resp

    @classmethod
    def edit_instance(cls, data: dict = None, user_id: str = None):
        resp = {
            "error": None,
            "message": None,
            "instance": None
        }

        data_keys = data.keys()

        for key in data_keys:
            if key not in cls.ALLOWED_PUT_FIELDS:
                resp["error"] = "Invalid Data"
                resp["message"] = f"Not allowed to alter field: '{key}' via this API."

                return resp

        user = cls.model.objects.filter(pk=user_id).first()
        user_data = cls.comp_serializer(instance=user).data

        for key in data_keys:
            user_data[key] = data.get(key)

        deserialized = cls.comp_serializer(instance=user, data=user_data)

        is_valid = deserialized.is_valid()

        if not is_valid:
            resp['error'] = "Serializer Invalid"
            resp['message'] = f"{deserialized.errors}."
            return resp

        deserialized.save()
        resp['message'] = f"User {deserialized.data.get('emai')} created successfully."
        resp['instance'] = deserialized.instance

        return resp

    @classmethod
    def delete_instance(cls, user_email: str = None, user_password: str = None, *args, **kwargs):
        resp = {
            "error": None,
            "message": None
        }

        user = cls.model.objects.filter(email=user_email).first()
        if not user:
            resp["error"] = "Not Found."
            resp["message"] = f"User with email:\t'{user_email}' not found."
            return resp

        if not user.authorize_password(password=user_password):
            resp["error"] = "Invalid credentials."
            resp["message"] = f"Password incorrect for user:\t'{user.email}'."
            return resp

        user.delete()
        resp["message"] = f"User '{user_email}' deleted successfully at {timezone.now()}"
        return resp

    @classmethod
    def login_user_via_password(cls, email: str = None, username: str = None, user_id: str = None, password: str = None, *args, **kwargs):
        resp = {
            "error": None,
            "message": None,
            "instance": None
        }

        if email and not username and not user_id:
            user = cls.model.objects.filter(email=email).first()
            if not user:
                resp["error"] = "Invalid credentials."
                resp["message"] = f"No user with eamil:\t'{email}' in system."
                return resp

        elif username and not email and not user_id:
            user = cls.model.objects.filter(username=username).first()
            if not user:
                resp["error"] = "Invalid credentials."
                resp["message"] = f"No user with username:\t'{username}' in system."
                return resp

        elif user_id and not email and not username:
            user = cls.model.objects.filter(pk=user_id).first()
            if not user:
                resp["error"] = "Invalid credentials."
                resp["message"] = f"No user with ID:\t'{user_id}' in system."
                return resp

        else:
            resp["error"] = "Invalid query parameters."
            resp["message"] = f"Please select either:\tUSERNAME or EMAIL or ID."
            return resp

        if not user.authorize_password(password=password):
            resp["error"] = "Invalid credentials."
            resp["message"] = f"Password incorrect for user:\t'{user.email}'."
            return resp

        tokens = cls.create_jwt_token(user=user)

        resp["message"] = f"User '{user.email}' successfully logged in via password at {timezone.now()}."
        resp['instance'] = tokens

        return resp

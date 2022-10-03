from django.utils import timezone

from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from user_app.api_helpers import UserAccountHelpers
from user_app.serializers import UserGeneralSerializer
from user_app import logger


class UserAccountCreationAPI(APIView):

    def post(self, request: Request, *args, **kwargs):

        resp = UserAccountHelpers.create_instance(data=request.data)

        if resp.get("error", None):
            del resp["instance"]
            return Response(
                resp,
                status=status.HTTP_400_BAD_REQUEST
            )

        if resp.get("instance", None):
            del resp["error"]
            resp["instance"] = UserGeneralSerializer(resp.get("instance")).data
            return Response(
                resp,
                status=status.HTTP_201_CREATED
            )


class UserLoginAPI(APIView):

    def post(self, request: Request, *args, **kwargs):
        resp = UserAccountHelpers.login_user_via_password(**request.data)
        if resp.get("error", None):
            del resp["instance"]
            return Response(
                resp,
                status=status.HTTP_400_BAD_REQUEST
            )

        if resp.get("instance", None):
            del resp["error"]
            return Response(
                resp,
                status=status.HTTP_200_OK
            )


class UserAccountAPI(APIView):
    """
    APIs for an user to view/edit/delete thir own account.
    """
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request, *args, **kwargs):
        """
        Get own account data.
        """
        user, _ = UserAccountHelpers.get_instance(
            identifier=request.user.id, param="id")

        if not user:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            UserAccountHelpers.io_serializer(user).data,
            status=status.HTTP_200_OK
        )

    def put(self, request: Request, *args, **kwargs):

        resp = UserAccountHelpers.edit_instance(**request.data)

        if resp.get("error", None):
            del resp["instance"]
            return Response(
                resp,
                status=status.HTTP_400_BAD_REQUEST
            )

        if resp.get("instance", None):
            del resp["error"]
            return Response(
                UserAccountHelpers.io_serializer(resp.get("instance")).data,
                status=status.HTTP_200_OK
            )

    def delete(self, request: Request, *args, **kwargs):

        if not request.data.get("user_email") == request.user.email:
            return Response(
                {
                    "error": "Email incorrect."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        resp = UserAccountHelpers.delete_instance(**request.data)

        if resp.get("error", None):
            return Response(
                resp,
                status=status.HTTP_400_BAD_REQUEST
            )

        del resp["error"]

        return Response(
            resp,
            status=status.HTTP_200_OK
        )


class AdminUserBasicAPI(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUser,)

    def get(self, request: Request, *args, **kwargs):
        logger.info(f"hit by user {request.user.email}")
        page = request.query_params.get("page")
        resp = UserAccountHelpers.search_instances(identifier="", page=page)

        return Response(
            resp,
            status=status.HTTP_200_OK
        )

    def delete(self, request: Request, *args, **kwargs):
        user_id = request.data.get("user")
        self_password = request.data.get("password")

        if not request.user.authorize_password(password=self_password):
            return Response(
                {
                    "error": "Password incorrect."
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        user, _ = UserAccountHelpers.get_instance(
            identifier=user_id, param="id")
        user.delete()

        return Response(
            {
                "success": f"User '{user_id}' was successfully deleted on {timezone.now().date()} at {timezone.now().time()}."
            },
            status=status.HTTP_200_OK
        )

from django.conf import settings
from django.core.paginator import Paginator
from django.utils import timezone

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from sample_app.models import SampleModel
from sample_app.serializers import SampleModelSerializer

from sample_app import logger


class SampleDataAPI(APIView):

    def get(self, request, page: int = 1, *args, **kwargs):

        if not request.query_params.get("id", None):
            """
                To return all (paginated) data in model.
            """
            qryset = SampleModel.objects.all()
            paginator = Paginator(qryset, settings.ITEMS_PER_PAGE)
            paginated = paginator.get_page(page)
            deserialized = SampleModelSerializer(paginated, many=True)
            return Response(
                deserialized.data,
                status=status.HTTP_200_OK
            )
        else:
            """
                To return a single data in model.
            """
            qryset = SampleModel.objects.filter(
                pk=request.query_params.get("id", None)).first()
            deserialized = SampleModelSerializer(qryset)
            return Response(
                deserialized.data,
                status=status.HTTP_200_OK
            )

    def post(self, request, *args, **kwargs):

        data = request.data
        deserialized = SampleModelSerializer(data=data)
        is_valid = deserialized.is_valid()

        if not is_valid:
            error = f"{deserialized.errors}"

            logger.warn(error)
            return Response(
                {
                    "error": error
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        deserialized.save()
        return Response(
            deserialized.data,
            status=status.HTTP_201_CREATED
        )

    def put(self, request, *args, **kwargs):
        item_id = request.query_params.get("id", None)
        if not item_id:
            error = f"'ID' is a mandatory field."
            logger.warn(error)
            return Response(
                {
                    "error": error
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        item = SampleModel.objects.filter(pk=item_id).first()
        if not item:
            error = f"Item <{item_id}> does not exist."
            logger.warn(error)
            return Response(
                {
                    "error": error
                },
                status=status.HTTP_404_NOT_FOUND
            )

        deserialized = SampleModelSerializer(
            instance=item, data=request.data)
        is_valid = deserialized.is_valid()

        if not is_valid:
            error = f"{deserialized.errors}"

            logger.warn(error)
            return Response(
                {
                    "error": error
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        deserialized.save()
        return Response(
            deserialized.data,
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, *args, **kwargs):

        item_id = request.data.get("id", None)
        if not item_id:
            error = f"'ID' is a mandatory field."
            logger.warn(error)
            return Response(
                {
                    "error": error
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            item = SampleModel.objects.get(pk=item_id)
        except SampleModel.DoesNotExist as ex:
            error = f"{ex}"
            logger.warn(error)
            return Response(
                {
                    "error": error
                },
                status=status.HTTP_404_NOT_FOUND
            )

        item.delete()
        resp = {
            "message": f"Item <{item_id}> has been deleted.>",
            "timestamp": f"{timezone.now()}"
        }

        return Response(
            resp,
            status=status.HTTP_200_OK
        )


class AlternateItemEditAPI(APIView):
    ALLOWED_FIELDS = (
        "name",
        "char_field",
        "decimal_field",
        "integer_field"
    )

    def put(self, request, *args, **kwargs):

        item_id = request.query_params.get("id", None)
        request_data = request.data
        if not item_id:
            error = f"'ID' is a mandatory field."
            logger.warn(error)
            return Response(
                {
                    "error": error
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        item = SampleModel.objects.filter(pk=item_id).first()
        if not item:
            error = f"Item <{item_id}> does not exist."
            logger.warn(error)
            return Response(
                {
                    "error": error
                },
                status=status.HTTP_404_NOT_FOUND
            )
        item_data = SampleModelSerializer(item).data

        for key in request_data.keys():
            if key not in self.ALLOWED_FIELDS:
                error = f"Not allowed to alter field: '{SampleModel.__name__}.{key}'."
                logger.warn(error)
                return Response(
                    {
                        "error": error
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            item_data[key] = request_data.get(key)

        deserialized = SampleModelSerializer(instance=item, data=item_data)
        is_valid = deserialized.is_valid()

        if not is_valid:
            error = f"{deserialized.errors}"

            logger.warn(error)
            return Response(
                {
                    "error": error
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        deserialized.save()
        return Response(
            deserialized.data,
            status=status.HTTP_201_CREATED
        )

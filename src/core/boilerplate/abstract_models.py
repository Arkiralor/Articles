from django.db import models
import uuid


class TemplateModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        default=uuid.uuid4,
        editable=False
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class TemplateModelUtils:
    model:models.Model = None
    op_serializer = None
    ip_serializer = None

    ALLOWED_PUT_FIELDS = tuple()
    GET_PARAM_CHOICES = tuple()

    @classmethod
    def search_instances(cls):
        pass

    @classmethod
    def get_instance(cls):
        pass

    @classmethod
    def create_instance(cls):
        pass

    @classmethod
    def edit_instance(cls):
        pass

    @classmethod
    def delete_instance(cls):
        pass


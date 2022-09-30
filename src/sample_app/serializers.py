from rest_framework.serializers import ModelSerializer
from sample_app.models import SampleModel


class SampleModelSerializer(ModelSerializer):

    def create(self, validated_data):
        instance, _ = SampleModel.objects.get_or_create(**validated_data)
        return instance

    class Meta:
        model = SampleModel
        fields = '__all__'

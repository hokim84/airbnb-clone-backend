from rest_framework.serializers import ModelSerializer
from .models import Photo, Video


class PhotoSerialzier(ModelSerializer):
    class Meta:
        model = Photo
        fields = (
            "pk",
            "file",
            "description",
        )

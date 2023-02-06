from rest_framework import serializers
from reviews.models import Review
from users.serializers import TinyUserSerialzier


class ReviewSerializer(serializers.ModelSerializer):

    user = TinyUserSerialzier(read_only=True)

    class Meta:
        model = Review
        fields = (
            "user",
            "payload",
            "rating",
        )

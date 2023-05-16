from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Amenity, Room
from medias.models import Photo, Video
from medias.serializers import PhotoSerialzier
from users.serializers import TinyUserSerialzier
from reviews.serializers import ReviewSerializer
from categories.serializers import CategorySerializer
from wishlists.models import WishList


class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "name",
            "description",
        )


class RoomListSerializer(ModelSerializer):

    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    photos = PhotoSerialzier(many=True, read_only=True)

    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
            "rating",
            "is_owner",
            "photos",
        )

    def get_rating(self, room):
        return room.rating()

    def get_is_owner(self, room):

        request = self.context["request"]
        return room.owner == request.user

    def get_photos(self, room):

        photos = Photo.objects.filter(pk=room.pk)


class RoomDetailSerializer(ModelSerializer):
    owner = TinyUserSerialzier(read_only=True)
    amenities = AmenitySerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    photos = PhotoSerialzier(many=True, read_only=True)

    class Meta:
        model = Room
        fields = "__all__"

    def get_rating(self, room):
        return room.rating()

    def get_is_owner(self, room):
        request = self.context["request"]
        return room.owner == request.user

    def get_is_liked(self, room):
        request = self.context["request"]
        if request.user.is_authenticated:
            return WishList.objects.filter(
                user=request.user, rooms__pk=room.pk
            ).exists()

        return False

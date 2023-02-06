from django.utils import timezone
import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from django.db import transaction
from .models import Amenity
from .models import Room
from reviews.models import Review
from reviews.serializers import ReviewSerializer
from categories.models import Category
from medias.models import Photo
from .serializers import AmenitySerializer, RoomListSerializer, RoomDetailSerializer
from config import settings
from medias.serializers import PhotoSerialzier
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from bookings.models import Booking
from bookings.serializers import PublicBookingSerializer, CreateRoomBookingSerializer


class Rooms(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        rooms = Room.objects.all()
        return Response(
            RoomListSerializer(
                rooms,
                many=True,
                context={"request": request},
            ).data
        )

    def post(self, request):
        serializer = RoomDetailSerializer(data=request.data)
        if serializer.is_valid():
            category_id = request.data.get("category")
            if not category_id:
                raise ParseError("Category is Reqrired")
            try:
                category = Category.objects.get(pk=category_id)
                if category.kind == Category.CategoryKindChoices.EXPERIENCE:
                    raise ParseError("Category should be Required")
            except Category.DoesNotExist:
                raise ParseError("Category not found")

            print("before atomic")
            try:
                with transaction.atomic():
                    print("inside of atomic")
                    room = serializer.save(
                        owner=request.user,
                        category=category,
                    )

                    print("save")

                    amenities = request.data.get("amenities")
                    print(amenities)
                    for amenity_pk in amenities:
                        print("Amenity::", amenity_pk)
                        amenity = Amenity.objects.get(pk=amenity_pk)
                        room.amenities.add(amenity)
                    return Response(RoomDetailSerializer(room).data)
            except Exception:
                raise ParseError("Ameniy not found!")
        else:
            return Response(serializer.errors)


class RoomDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            room = Room.objects.get(pk=pk)
            return room
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(
            room,
            context={"request": request},
        )
        return Response(serializer.data)

    def put(self, request, pk):
        room = self.get_object(pk)
        user = request.user

        serializer = RoomDetailSerializer(room, data=request.data, partial=True)
        if serializer.is_valid():
            amenities = request.data.get("amenities")
            if amenities:
                for amenity_pk in amenities:
                    amenity = Amenity.objects.get(amenity_pk)
                    room.amenities.add(amenity)
            return Response(RoomDetailSerializer(room).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        room = self.get_object(pk)
        room.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Amenities(APIView):
    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = AmenitySerializer(all_amenities, many=True)
        return Response(serializer.data)

    def post(self, reqeust):
        serializer = AmenitySerializer(data=reqeust.data)
        if serializer.is_valid():
            amenity = serializer.save()
            return Response(AmenitySerializer(amenity).data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class AmenityDetail(APIView):
    def get_object(self, pk):
        try:
            amenity = Amenity.objects.get(pk=pk)
            return amenity
        except Amenity.DoesNotExist:
            raise NotFound

    def get(self, reqeust, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(amenity)
        return Response(serializer.data)

    def put(self, reqeust, pk):
        amenity = self.get_object(pk)
        serialzier = AmenitySerializer(
            instance=amenity,
            data=reqeust.data,
            partial=True,
        )
        if serialzier.is_valid():
            updated_amenity = serialzier.save()
            return Response(AmenitySerializer(updated_amenity).data)
        else:
            return Response(serialzier.errors, HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class RoomReviews(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1

        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size

        room = self.get_object(pk)
        serializer = ReviewSerializer(
            room.reviews.all()[start:end],
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save(user=request.user, room=self.get_object(pk))
            serializer = ReviewSerializer(review)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class RoomAmenities(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1

        page_size = 2
        start = (page - 1) * page_size
        end = start + page_size
        room = self.get_object(pk)
        serializer = AmenitySerializer(
            room.amenities.all()[start:end],
            many=True,
        )
        return Response(serializer.data)


class RoomPhotos(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            room = Room.objects.get(pk=pk)
            return room
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = PhotoSerialzier(
            room.photos.all(),
            many=True,
        )

        print(serializer.data)

        return Response(serializer.data)

    def post(self, reqeust, pk):

        room = self.get_object(pk)

        if reqeust.user != room.owner:
            raise PermissionDenied

        serializer = PhotoSerialzier(data=reqeust.data)
        if serializer.is_valid():
            photo = serializer.save(
                room=room,
            )
            serializer = PhotoSerialzier(photo)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class RoomBookings(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        now = timezone.localtime(timezone.now()).date()

        bookings = Booking.objects.filter(
            room=room,
            kind=Booking.BookingKindChoice.ROOM,
            check_in__gt=now,
        )
        serializer = PublicBookingSerializer(bookings, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        room = self.get_object(pk)
        serialzier = CreateRoomBookingSerializer(data=request.data)
        if serialzier.is_valid():
            booking = serialzier.save(
                user=request.user,
                room=room,
                kind=Booking.BookingKindChoice.ROOM,
            )
            serialzier = PublicBookingSerializer(booking)
            return Response(serialzier.data)
        else:
            return Response(serialzier.errors)

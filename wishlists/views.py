from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import WishList
from rest_framework.exceptions import NotFound
from .serializers import WishlistSerializer
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_200_OK
from rooms.models import Room

# Create your views here.


class Wishlists(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        all_wishlist = WishList.objects.filter(user=request.user)
        serializer = WishlistSerializer(
            all_wishlist,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    def post(self, request):
        serialzier = WishlistSerializer(
            user=request.user,
            context={"request": request},
        )
        if serialzier.is_valid():
            wishlist = serialzier.save()
            return Response(WishlistSerializer(wishlist).data)
        else:
            return Response(serialzier.errors)


class WishlistDetail(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return WishList.objects.get(pk=pk, user=user)
        except WishList.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        serilalizer = WishlistSerializer(
            wishlist,
            context={"request": request},
        )
        return Response(serilalizer.data)

    def delete(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        wishlist.delete()
        Response(status=HTTP_200_OK)

    def put(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        serializer = WishlistSerializer(
            wishlist,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        if serializer.is_valid():
            updated_wishlist = serializer.save()
            return Response(WishlistSerializer(updated_wishlist).data)
        else:
            return Response(serializer.errors)


class WishlistToggle(APIView):
    permission_classes = [IsAuthenticated]

    def get_list(self, pk, user):
        try:
            return WishList.objects.get(pk=pk, user=user)
        except WishList.DoesNotExist:
            raise NotFound

    def get_room(self, room_pk):
        try:
            return Room.objects.get(pk=room_pk)
        except Room.DoesNotExist:
            raise NotFound

    def put(self, request, pk, room_pk):
        wishlist = self.get_list(pk, request.user)
        room = self.get_room(room_pk)
        if wishlist.rooms.filter(pk=room.pk).exists():
            wishlist.rooms.remove(room)
        else:
            wishlist.rooms.add(room)

        return Response(status=HTTP_200_OK)

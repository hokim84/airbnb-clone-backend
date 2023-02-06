from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_204_NO_CONTENT
from .serializer import PerkSerializer
from .models import Perk


class Perks(APIView):
    def get(self, reqeust):
        all_perks = Perk.objects.all()
        serializer = PerkSerializer(all_perks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PerkSerializer(data=request.data)
        if serializer.is_valid():
            perk = serializer.save()
            return Response(PerkSerializer(perk).data)
        else:
            return Response(serializer.errors)


class PerkDetail(APIView):
    def get_object(self, pk):
        try:
            perk = Perk.objects.get(pk=pk)
            return perk
        except Perk.DoesNotExist:
            raise NotFound

    def get(self, reqeust, pk):
        perk = self.get_object(pk)
        return Response(PerkSerializer(perk).data)

    def put(self, reqeust, pk):
        perk = self.get_object(pk)
        serializer = PerkSerializer(instance=perk, data=reqeust.data, partial=True)
        if serializer.is_valid():
            update_perk = serializer.save()
            return Response(PerkSerializer(update_perk).data)
        else:
            return Response(serializer.errors)

    def delete(self, reqeust, pk):
        perk = self.get_object(pk)
        perk.delete()
        return Response(HTTP_204_NO_CONTENT)

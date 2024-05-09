from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .models import Player
from .serializers import PlayerSerializer

from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

def lobby(request):
    template = loader.get_template('lobby.html')
    return HttpResponse(template.render())

class ListCreatePlayerView(ListCreateAPIView):
    model = Player
    serializer_class = PlayerSerializer

    def get_queryset(self):
        return Player.objects.all()
    
    def create(self, request, *args, **kwargs):
        serializer = PlayerSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                "Message": "Create new player successful!"
            }, status = status.HTTP_201_CREATED)
        
        return Response({
            "Message": "Create new player unsuccessful!"
        }, status = status.HTTP_400_BAD_REQUEST)
    
class UpdateDeletePlayerView(RetrieveUpdateDestroyAPIView):
    model = Player
    serializer_class = PlayerSerializer

    def get_queryset(self):
        return Player.objects.all()

    def put(self, request, *args, **kwargs):
        player = get_object_or_404(Player, id=kwargs.get('pk'))
        serializer = PlayerSerializer(player,data=request.data, partial=True) # Partial cho phép cập nhật những data cần thiết

        if serializer.is_valid():
            serializer.save()

            return Response({
                'message': 'Update player successful!'
            }, status=status.HTTP_200_OK)

        return Response({
            'message': 'Update player unsuccessful!'
        }, status=status.HTTP_400_BAD_REQUEST)

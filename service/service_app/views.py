from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Player
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


# Create your views here.

def lobby(request):
    template = loader.get_template('lobby.html')
    return HttpResponse(template.render())


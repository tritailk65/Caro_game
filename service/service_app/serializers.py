from rest_framework import serializers
from models import Player

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('ingame_name', 'joined_date' , 'score', 'game_win' ,'game_lose', 'game_draw')
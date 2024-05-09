from django.db import models

# Create your models here.
class Player(models.Model):
    id = models.AutoField(primary_key=True)
    ingame_name = models.CharField(max_length=255)
    joined_date = models.DateField(null=True)
    score = models.IntegerField(auto_created=0,null=True)
    game_win =models.IntegerField(null=True)
    game_lose = models.IntegerField(null=True)
    game_draw = models.IntegerField(null=True)

    def __str__(self):
        return f"ID: {self.id} - Name: {self.ingame_name}"
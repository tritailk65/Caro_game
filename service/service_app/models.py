from django.db import models

# Create your models here.
class Player(models.Model):
    ingame_name = models.CharField(max_length=255)
    joined_date = models.DateField(null=True)

    def __str__(self):
        return f"{self.ingame_name}"
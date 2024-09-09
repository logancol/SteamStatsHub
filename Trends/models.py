from django.db import models

# Create your models here.

from django.db import models


# Django model for game data. This will be updated daily using Django Q.
# For earlier versions of the site, player data will be limited to a pre-defined 500 games, (chosen based on popularity at time of creation)
from django.db import models
from django.utils import timezone

class PlayerCount(models.Model):
    game_id = models.CharField(max_length=50)
    game_name = models.CharField(max_length=255)  # Store game name
    player_count = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically add the current time

    class Meta:
        indexes = [
            models.Index(fields=['game_name']),
            models.Index(fields=['timestamp']),
        ]
    
    def __str__(self):
        return f"{self.game_name} - {self.player_count} players at {self.timestamp}"
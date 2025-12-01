from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Game(models.Model):
    room_name = models.CharField(max_length=100, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_games')
    board = models.CharField(max_length=9, default=' ' * 9)  # ' ' * 9 para un tablero vacío
    active_player = models.IntegerField(default=1)  # 1 o 2
    game_state = models.CharField(max_length=20, default='active')  # 'active', 'won', 'tie'
    winner = models.IntegerField(null=True, blank=True)  # 1, 2 o None

    def __str__(self):
        return self.room_name
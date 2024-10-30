from django.db import models

from django.contrib.auth.models import User

class Watchlist(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    itemID = models.PositiveIntegerField(primary_key = True)
    itemType = models.CharField(max_length=10)
    addedOn = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username.username} - {self.itemID}"
        
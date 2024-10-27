from django.db import models

from django.contrib.auth.models import User

class Watchlist(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    itemID = models.PositiveIntegerField(primary_key = True)
    itemName = models.CharField(max_length=100)
    itemPoster = models.CharField(max_length=250)
    itemRating = models.FloatField()
    itemType = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.username.username} - {self.itemName}"

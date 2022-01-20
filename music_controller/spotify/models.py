from django.db import models
from api.models import Room

#model to store a token for each host of room
class SpotifyToken(models.Model):
    user = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    access_token = models.CharField(max_length=150)
    refresh_token = models.CharField(max_length=150)
    expires_in = models.DateTimeField()
    token_type = models.CharField(max_length=50)

class Vote(models.Model): #creates a model to store each vote and the data associated with that vote
    user = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    song_id = models.CharField(max_length=50)
    room = models.ForeignKey(Room, on_delete=models.CASCADE) #foreign key means we can just pass an instance of another object in this case the Room object and this stores a reference to that room object which is faster than filetering from Room.objects each time, on delete means if the room gets deleted all of these vote objects also get deleted
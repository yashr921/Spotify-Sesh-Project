from django.db import models
import string
import random

def generate_unique_code():
    length = 6

    while True:
        #generates a random code of upercase letters of length 6
        code = ''.join(random.choices(string.ascii_uppercase, k=length))
        if Room.objects.filter(code=code).count() == 0: #gets all the code objects from the rooms and counts the number of code objects that are the same as this one, if the count is 0 that means there are no code objects that are the same as this one so returns this code
            break
    return code

#Model for room, which controls the host's music
class Room(models.Model):
    code = models.CharField(max_length=8, default=generate_unique_code, unique=True) #unique ID for room
    host = models.CharField(max_length=50, unique=True) #info that relates to the host
    guest_can_pause = models.BooleanField(null=False, default=False) #boolean value whether the guest can skip a song
    votes_to_skip = models.IntegerField(null=False, default=1) #min votes needed to skip a song
    created_at = models.DateTimeField(auto_now_add=True)
    current_song = models.CharField(max_length=50, null=True)
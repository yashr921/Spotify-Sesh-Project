#takes the models and transforms them into a JSON response, can work both ways
from rest_framework import serializers
from .models import Room

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        #id is a unique integer for each model
        fields = ('id', 'code', 'host', 'guest_can_pause', 'votes_to_skip', 'created_at')

#The view will send a POST request to this serializer which makes sure the data being sent to the post request is valid and gives it in a valid python format for the database
class CreateRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('guest_can_pause', 'votes_to_skip')

class UpdateRoomSerializer(serializers.ModelSerializer):
    code = serializers.CharField(validators=[]) #since code field in model is unique can't pass in the same code so instead code references this char field

    class Meta:
        model = Room
        fields = ('guest_can_pause', 'votes_to_skip','code')

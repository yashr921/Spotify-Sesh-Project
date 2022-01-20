from django.db.models import query
from django.db.models.query_utils import select_related_descend
from django.shortcuts import render
from django.http import JsonResponse

#This is where the endpoints are written
#An endpoint is anything after the / it is just the location on the server the user is visiting

#Whenever you have a web server there is an incoming request that goes through an endpoint which returns a response

from rest_framework import generics, status
from rest_framework import response
from rest_framework.serializers import Serializer
from .serializers import RoomSerializer, CreateRoomSerializer, UpdateRoomSerializer
from .models import Room
from rest_framework.views import APIView
from rest_framework.response import Response

#this class allows us to view all the rooms and create a room
class RoomView(generics.ListAPIView):
    queryset = Room.objects.all() #query set of all the room objects
    serializer_class = RoomSerializer #class to return JSON response

class GetRoom(APIView):
    serializer_class = RoomSerializer
    lookup_url_kwarg = 'code' #need to pass a paramter in the url called code which will be equal to the room we are trying to get

    def get(self, request, format=None):
        code = request.GET.get(self.lookup_url_kwarg) #request.GET gets info about the URL from the get request and .get([parameter]) gets the parameter that matches the name 'code'
        if code != None:
            room = Room.objects.filter(code=code) #this looks up the room using the code and returns that
            if len(room) > 0:
                data = RoomSerializer(room[0]).data #serializes the room and gets the data from that, returns as a python dictionary
                data['is_host'] = self.request.session.session_key == room[0].host #current session key is the user that sent this request and checks if it matches the host of the room and sets the value to true or false based on that
                return Response(data, status=status.HTTP_200_OK)
            return Response({'No Room Found' : 'Invalid Room Code'}, status=status.HTTP_404_NOT_FOUND) #returns if room == None meaning the room was not found
        return Response({'Bad Request' : 'Code parameter not found in request'}, status=status.HTTP_400_BAD_REQUEST) #returns if code == None meaning no code was entered

#class that sends a post request that the user is joining the room
class JoinRoom(APIView):
    lookup_url_kwarg = 'code' 

    def post(self, request, format=None):
        #checks if user already has an active session, if they don't then create one
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        #gets code from the post request, we use .data to get the data from the post request
        code = request.data.get(self.lookup_url_kwarg)
        if code != None:
            room_result = Room.objects.filter(code=code)
            if len(room_result) > 0:
                room = room_result[0] #gets the room from the room dictionary
                self.request.session['room_code'] = code #sets the room code variable for the session which stores the room code for the room they are currently in and takes them back to that same room upon site reload
                return Response({'message':'Room Joined'}, status=status.HTTP_200_OK)
            return Response({'Bad Request':'Invalid Room Code'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'Bad Request': 'Invalid host data, did not find a room code'}, status=status.HTTP_400_BAD_REQUEST)
            

    
#passing APIView allows us to overwrite some default methods
class CreateRoomView(APIView):
    serializer_class = CreateRoomSerializer

    def post(self, request, format=None):
        """
        Method to post to the serializer
        takes in a request
        """
        #checks if user already has an active session, if they don't then create one
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        
        #gets data from the request and serializes
        serializer = self.serializer_class(data=request.data)
        #if the data is valid then gets the data to create the room
        if serializer.is_valid():
            guest_can_pause = serializer.data.get('guest_can_pause')
            votes_to_skip = serializer.data.get('votes_to_skip')
            host = self.request.session.session_key
            queryset = Room.objects.filter(host=host) #checks if there is already a room with that same host
            if queryset.exists(): #if room with same host exists then just updates guest can pause and votes to skip values for that room
                room = queryset[0]
                room.guest_can_pause = guest_can_pause
                room.votes_to_skip = votes_to_skip
                room.save(update_fields=['guest_can_pause', 'votes_to_skip'])
                self.request.session['room_code'] = room.code
                return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)
            else: #if no room with that host exists then creates a new one
                room = Room(host=host, guest_can_pause=guest_can_pause, votes_to_skip=votes_to_skip)
                room.save()
                self.request.session['room_code'] = room.code
                return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)
        
        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST) #returns error if neither of those two is possible

class UserInRoom(APIView):
    
    #this method gets the room code from the current session if there is one, if there is not then it returns null
    def get(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        data = {
            'code': self.request.session.get('room_code')
        }
        return JsonResponse(data, status=status.HTTP_200_OK)

class LeaveRoom(APIView):

    #method to remove the user from this room and if user is the host deletes the room
    def post(self, request, format=None):
        if 'room_code' in self.request.session:
            self.request.session.pop('room_code')
            host_id = self.request.session.session_key
            room = Room.objects.get(host=host_id)
            if room:
                room.delete()
        return Response({'Message': 'Success'}, status=status.HTTP_200_OK)

class UpdateRoom(APIView):
    serializer_class = UpdateRoomSerializer

    def patch(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            guest_can_pause = serializer.data.get('guest_can_pause')
            votes_to_skip = serializer.data.get('votes_to_skip')
            code = serializer.data.get('code')

            queryset = Room.objects.filter(code=code)
            if not queryset.exists():
                return Response({"msg" : 'Room not found'}, status=status.status.HTTP_404_NOT_FOUND)
            room = queryset[0]
            user_id = self.request.session.session_key
            if room.host != user_id:
                return Response({"msg" : 'You are not host of this room'}, status=status.status.status.HTTP_403_FORBIDDEN)
            room.guest_can_pause = guest_can_pause
            room.votes_to_skip = votes_to_skip
            room.save(update_fields=['guest_can_pause', 'votes_to_skip'])
            return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)

        return Response({"Bad Request": "Invalid Data..."}, status=status.HTTP_400_BAD_REQUEST)

        
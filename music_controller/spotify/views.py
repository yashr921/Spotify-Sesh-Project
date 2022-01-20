# from urllib import response
# from urllib.request import Request
# from django.shortcuts import render, redirect
# from .credentials import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
# from rest_framework.views import APIView
# from requests import Request,post
# from rest_framework import status
# from rest_framework.response import Response
# from .util import update_or_create_user_tokens, is_spotify_authenticated

# class AuthURL(APIView):

#     #returns a url that we can go to to authenticate our spotify app
#     def get (self, request, format=None):
#         scopes = 'user-read-playback-state user-modify-playback-state user-read-currently-playing' #the scopes that we want to access with our app

#         url = Request('GET', 'https://accounts.spotify.com/authorize', params={
#             'scope': scopes,
#             'response_type': 'code',
#             'redirect_uri': REDIRECT_URI,
#             'client_id': CLIENT_ID,
#         }).prepare().url
#         print("returning url")
#         return Response({'url', url}, status=status.HTTP_200_OK)

# #uses the url to send a request to get the access and refresh tokens
# def spotify_callback(request, format=None):
#     print("spotify callback called")
#     code = request.GET.get('code') #code used to authenticate user/ get access token
#     error = request.GET.get('error') #error message if there is an error
    
#     response = post('https://accounts.spotify.com/api/token', data={
#         'grant_type': 'authorization_code',
#         'code': code,
#         'redirect_uri': REDIRECT_URI,
#         'client_id': CLIENT_ID,
#         'client_secret': CLIENT_SECRET
#     }).json() #after we get the url (code) we send this response to spotify to get the access and refresh token

#     access_token = response.get('access_token')
#     token_type = response.get('token_type')
#     refresh_token = response.get('refresh_token')
#     expires_in = response.get('expires_in')
#     error = response.get('error')

#     if not request.session.exists(request.session.session_key):
#             request.session.create()
    
#     update_or_create_user_tokens(request.session.session_key, access_token, token_type, expires_in, refresh_token) #updates database with access token and other info
#     return redirect('frontend:')

# class IsAuthenticated(APIView):
#     def get(self, request, format=None):
#         is_authenticated = is_spotify_authenticated(self.request.session.session_key)
#         return Response({'status': is_authenticated}, status=status.HTTP_200_OK)

from operator import is_
from django.shortcuts import redirect
from .credentials import REDIRECT_URI, CLIENT_SECRET, CLIENT_ID
from rest_framework.views import APIView
from requests import Request, post
from rest_framework import status
from rest_framework.response import Response
from .util import *
from api.models import Room
from .models import Vote


class AuthURL(APIView):
    def get(self, request, fornat=None):
        scopes = 'user-read-playback-state user-modify-playback-state user-read-currently-playing'

        url = Request('GET', 'https://accounts.spotify.com/authorize', params={
            'scope': scopes,
            'response_type': 'code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID
        }).prepare().url

        return Response({'url': url}, status=status.HTTP_200_OK)


def spotify_callback(request, format=None):
    code = request.GET.get('code')
    error = request.GET.get('error')

    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    error = response.get('error')

    if not request.session.exists(request.session.session_key):
        request.session.create()

    update_or_create_user_tokens(
        request.session.session_key, access_token, token_type, expires_in, refresh_token)

    return redirect('frontend:')


class IsAuthenticated(APIView):
    def get(self, request, format=None):
        is_authenticated = is_spotify_authenticated(
            self.request.session.session_key)
        return Response({'status': is_authenticated}, status=status.HTTP_200_OK)

class CurrentSong(APIView):
    def get(self, request, format=None):
        room_code = self.request.session.get('room_code')
        room = Room.objects.filter(code=room_code)
        if room.exists():
            room = room[0]
        else:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        host = room.host
        endpoint = "player/currently-playing"
        response = execute_spotify_api_request(host, endpoint)

        if 'error' in response or 'item' not in response:
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        item = response.get('item')
        duration = item.get('duration_ms')
        progress = response.get('progress_ms')
        album_cover = item.get('album').get('images')[0].get('url')
        is_playing = response.get('is_playing')
        song_id = item.get('id')

        artist_string = ""

        for i, artist in enumerate(item.get('artists')): #if there are multiple artists it comes in the form of a list so just converts list into one string
            if i > 0:
                artist_string += ", "
            name = artist.get('name')
            artist_string += name

        votes = len(Vote.objects.filter(room=room, song_id=song_id)) #gets vote objects for this song

        song = {
            'title': item.get('name'),
            'artist': artist_string,
            'duration': duration,
            'time': progress,
            'image_url': album_cover,
            'is_playing': is_playing,
            'votes': votes,
            'votes_required': room.votes_to_skip,
            'id': song_id
        }

        self.update_room_song(room, song_id)
        return Response(song, status=status.HTTP_200_OK)

    def update_room_song(self, room, song_id): #updates the current song field of the room and deletes all the vote objects for the current song
        current_song = room.current_song

        if current_song != song_id:
            room.current_song = song_id
            room.save(update_fields=['current_song']) #updates the song id
            votes = Vote.objects.filter(room=room).delete() #deletes the vote objects

class PauseSong(APIView):
    def put(self, request, format=None):
        room_code = self.request.session.get('room_code')
        room = Room.objects.get(code=room_code)
        if self.request.session.session_key == room.host or room.guest_can_pause: #checks if user is host or guests can pause
            pause_song(room.host)
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        return Response({}, status=status.HTTP_403_FORBIDDEN)

class PlaySong(APIView):
    def put(self, request, format=None):
        room_code = self.request.session.get('room_code')
        room = Room.objects.get(code=room_code)
        if self.request.session.session_key == room.host or room.guest_can_pause: #checks if user is host or guests can pause
            play_song(room.host)
            return Response({}, status=status.HTTP_204_NO_CONTENT)
            
        return Response({}, status=status.HTTP_403_FORBIDDEN)

class SkipSong(APIView):
    def post(self, request, format=None): #post request because the database is being upddate
        room_code = self.request.session.get('room_code')
        room = Room.objects.get(code=room_code)
        votes = Vote.objects.filter(room=room, song_id=room.current_song) #gets the votes for the current song
        votes_needed = room.votes_to_skip

        if self.request.session.session_key == room.host or len(votes) + 1 >= votes_needed: #if user is host or # of votes + 1 for the current vote is greater than votes needed then skips song
            votes.delete() #deletes all the votes for the current song
            skip_song(room.host)
        else: #otherwise create a new vote object
            if len(Vote.objects.filter(room=room, song_id=room.current_song, user=self.request.session.session_key)) == 0:
                vote = Vote(user=self.request.session.session_key, room=room, song_id=room.current_song) #creates vote object
                vote.save() #saves vote to database
        return Response({}, status=status.HTTP_204_NO_CONTENT)
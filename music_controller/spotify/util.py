from urllib import response
from urllib.request import Request
from .models import SpotifyToken
from django.utils import timezone
from datetime import timedelta
from .credentials import CLIENT_ID, CLIENT_SECRET
from requests import post,get,put

BASE_URL = "https://api.spotify.com/v1/me/"

def get_user_tokens(session_key): #checks if user token already exists
    user_tokens = SpotifyToken.objects.filter(user=session_key)
    if user_tokens.exists():
        return user_tokens[0]
    else:
         return None


def update_or_create_user_tokens(session_key, access_token, token_type, expires_in, refresh_token):
    tokens = get_user_tokens(session_key)
    #expires in has value of 3600 (seconds)
    expires_in = timezone.now() + timedelta(seconds=expires_in) #converts expired in to an actual date time value based on the user's timezone

    if tokens: #if token exists updates its fields
        tokens.access_token = access_token
        tokens.refresh_token = refresh_token
        tokens.expires_in = expires_in
        tokens.token_type = token_type
        tokens.save(update_fields=['access_token', 'refresh_token', 'expires_in', 'token_type'])
    else: #if token doesn't exist creates a new entry
        tokens = SpotifyToken(user=session_key, access_token=access_token,refresh_token=refresh_token, expires_in=expires_in)
        tokens.save()

#if token is expired refreshs it and returns true, otherwise returns false if token is not authenticated
def is_spotify_authenticated(session_key):
    tokens = get_user_tokens(session_key)

    if tokens:
        expiry = tokens.expires_in
        if expiry <= timezone.now(): #checks if token is not expired (checks if expiry time is less than current time)
            refresh_spotify_token(session_key)
        return True
    return False

#refreshs the spotify token
def refresh_spotify_token(session_id):
    refresh_token = get_user_tokens(session_id).refresh_token

    response = post('https://accounts.spotify.com/api/token', data={ #sends post request to spotify api to get refresh token
        'grant_type': 'refresh_token', #telling spotify what data type to expect
        'refresh_token': refresh_token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    expires_in = response.get('expires_in')

    update_or_create_user_tokens(
        session_id, access_token, token_type, expires_in, refresh_token) #updates database with new token

#helper function to handle all requests to the spotify API
def execute_spotify_api_request(session_id, endpoint, post_=False, put_=False):
    token = get_user_tokens(session_id)
    headers = {'Content-Type': 'application/json', 'Authorization': "Bearer " + token.access_token}

    if post_:
        post(BASE_URL + endpoint, headers=headers)
    if put_:
        put(BASE_URL + endpoint, headers=headers)
    
    response = get(BASE_URL + endpoint, {}, headers=headers)

    try:
        return response.json()
    except:
        return {'Error': 'Issue with request'}

def play_song(session_id):
    return execute_spotify_api_request(session_id, 'player/play', put_=True)

def pause_song(session_id):
    return execute_spotify_api_request(session_id, 'player/pause', put_=True)

def skip_song(session_id):
    return execute_spotify_api_request(session_id, 'player/next', post_=True)
from django.urls import path
from .views import index

app_name = 'frontend'

urlpatterns = [
    path('', index, name=''), #this will render the index template whenever we have the blank path, need to include name so redirects from other folders can know which path to redirect to
    path('join', index),
    path('create', index),
    path('room/<str:roomCode>', index)
]

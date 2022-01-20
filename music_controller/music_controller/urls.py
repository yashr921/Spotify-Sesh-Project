"""music_controller URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django import urls
from django.contrib import admin
from django.urls import path, include
"""
1. whenever the user types in a url e.g. domain.com/hello the part after the / is sent to this file
2. this file then dispatches these URLs to the correct applications, the admin path below sends anything under the admin url to admin.site.urls which handles that url
then this function
"""
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')), #the blank prefix means it will send any url to api.urls
    path('', include('frontend.urls')), #this sends any url that is not admin or api to the frontend.urls to be handled there
    path('spotify/', include('spotify.urls'))
]

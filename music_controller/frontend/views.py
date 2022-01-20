from django.shortcuts import render

#In this file we are going to render the index template

def index(request, *args, **kwargs):
    """
    This function takes a request and returns a render of the template
    *args is the source file for the template
    """
    return render(request, 'frontend/index.html')
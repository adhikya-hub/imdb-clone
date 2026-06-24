import requests
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.template import response


def home(request):
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={settings.TMDB_API_KEY}"
    response = requests.get(url)
    movies = response.json()
    return render(request, "movies/home.html", {"movies": movies["results"]})


# import requests
# from django.conf import settings
# from django.http import HttpResponse


# def home(request):
#     url = f"https://api.themoviedb.org/3/movie/popular?api_key={settings.TMDB_API_KEY}"

#     response = requests.get(url)

#     return HttpResponse(f"Status: {response.status_code}<br><br>{response.text}")

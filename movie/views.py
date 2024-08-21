from django.shortcuts import render
from django.http import HttpResponse
import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64

from .models import Movie

# Create your views here.
def home(request):
  searchTerm = request.GET.get('searchMovie')
  if searchTerm:
    movies = Movie.objects.filter(title__icontains=searchTerm)
  else:
    movies = Movie.objects.all()

  return render(request, 'home.html', {
    'name': "Juan Pablo",
    'searchTerm': searchTerm,
    'movies': movies
  })

def about(request):
  return render(request, 'about.html')

def statistics_view(request):
    matplotlib.use('Agg')

    all_movies = Movie.objects.all()

    movie_counts_by_year = {}
    for movie in all_movies:
        year = movie.year if movie.year else "None"
        if year in movie_counts_by_year:
            movie_counts_by_year[year] += 1
        else:
            movie_counts_by_year[year] = 1

    #Grafica de películas por año
    bar_width = 0.5
    bar_positions = range(len(movie_counts_by_year))
    
    plt.figure(figsize=(10, 5))
    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align='center')
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    
    image_png = buffer.getvalue()
    buffer.close()
    graphic_year = base64.b64encode(image_png).decode('utf-8')

    movie_counts_by_genre = {}
    for movie in all_movies:
        if movie.genre:
            genre = movie.genre.split(',')[0]
            if genre in movie_counts_by_genre:
                movie_counts_by_genre[genre] += 1
            else:
                movie_counts_by_genre[genre] = 1

    #Grafica de películas por género
    plt.figure(figsize=(10, 5))
    bar_positions_genre = range(len(movie_counts_by_genre))
    
    plt.bar(bar_positions_genre, movie_counts_by_genre.values(), width=bar_width, align='center')
    plt.title('Movies by Genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions_genre, movie_counts_by_genre.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    
    image_png_genre = buffer.getvalue()
    buffer.close()
    graphic_genre = base64.b64encode(image_png_genre).decode('utf-8')

    return render(request, 'statistics.html', {'graphic_year': graphic_year, 'graphic_genre': graphic_genre})

def signup(request):
   email = request.GET.get('email')
   return render(request, 'signup.html', {'email':email})
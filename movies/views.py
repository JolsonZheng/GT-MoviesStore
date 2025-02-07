from django.shortcuts import render
from .models import Movie

def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term) #filter movies based on the search term
    else:
        movies = Movie.objects.all() #retrieve all movies if no search term is provided

    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies
    return render(request, 'movies/index.html', {'template_data': template_data})

def show(request, id):
    movie = Movie.objects.get(id=id) #retrieve a specific movie based on its id

    template_data = {}
    template_data['title'] = movie.name #now access movie.name as an object attribute
    template_data['movie'] = movie
    return render(request, 'movies/show.html', {'template_data': template_data})

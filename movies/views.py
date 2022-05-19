from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Movie
from users.models import MovieList

# Create your views here.
@login_required(login_url='login')
def moviesView(request):
    usermovies = MovieList.objects.filter(user_id=request.user.id)
    movies = [Movie.objects.get(id=movie.movie_id) for movie in usermovies]

    context = {
        'movies': movies
    }

    # return render(request, 'list_summary.html', context)
    return render(request, 'detail_list.html', context)
    
@login_required(login_url='login')
def movieListDetailView(request, state):
    STATES = {
        'completas' : ['Completada','completadas'],
        'en-proceso' : ['En proceso', 'en proceso'],
        'abandonadas' : ['Abandonada', 'abandonadas'],
        'en-espera' : ['En espera', 'en lista de espera'],
    }
    toast = ''

    if request.method == 'POST':
        user = request.user
        toast_title = ''

        if 'movie_id' in request.POST.keys() and request.POST['new_state'] in ('Completada', 'En proceso', 'Abandonada', 'En espera'):
            movie_id = request.POST['movie_id']
            movie = MovieList.objects.get(user_id=user.id, movie_id=movie_id)

            movie.state = request.POST['new_state']
            movie.save()
            user.save()
            toast_title = f"'{Movie.objects.get(id=movie_id).title}' ha sido editado con éxito."
            print(request.POST);

        elif 'delete_id' in request.POST.keys():
            movie_id = request.POST['delete_id']
            movie = Movie.objects.get(id=movie_id)
            user.movies.remove(movie)
            user.save()
            toast_title = f"'{movie.title}' ha sido eliminado con éxito."
        
        toast = '''Swal.mixin({{
                    title: "{toast_title}",
                    toast: true,
                    position: 'bottom-right',
                    showConfirmButton: false,
                    timer: 3000,
                    timerProgressBar: true,
                    didOpen: (toast) => {{
                        toast.addEventListener('mouseenter', Swal.stopTimer)
                        toast.addEventListener('mouseleave', Swal.resumeTimer)
                    }},
                    customClass: {{
                        container: 'toast',
                    }},
                    background: '#CDF8B8',
                    color: '#958CAB',
                    target: '#toast_target'
                }})'''.format_map({'toast_title': toast_title, })

    usermovies = MovieList.objects.filter(user_id=request.user.id, state=STATES[state][0])
    movies = [Movie.objects.get(id=movie.movie_id) for movie in usermovies]

    context = {
        'state': STATES[state][0],
        'title': STATES[state][1],
        'movies': movies,
        'toast': toast,
    }

    return render(request, 'detail_list.html', context)

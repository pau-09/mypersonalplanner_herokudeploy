import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Book
from users.models import BookList

@login_required(login_url='login')
def booksView(request):
    '''
        Books general view
        Will display 3 grafics
            1. Count of each list books
            2. Count of distinct authors
    '''
    
    statesData = _get_books_states_count_as_json(request.user)
    authorsData = _get_authors_count_as_json(request.user)
    genresData = _get_genres_count_as_json(request.user)

    context = {
        'entry_type': 'libros',
        'statesData': statesData,
        'authorsData': authorsData,
        'genresData': genresData,
    }

    return render(request, 'list_summary.html', context)
    
@login_required(login_url='login')
def bookListDetailView(request, state):
    STATES = {
        'completos': ['Completado','completados'],
        'en-proceso': ['En proceso', 'en proceso'],
        'abandonados': ['Abandonado', 'abandonados'],
        'en-espera': ['En espera', 'en lista de espera'],
    }
    toast = ''
    user_booklist = list()

    if request.method == 'POST':
        user = request.user
        toast_title = ''
        request_keys = request.POST.keys()

        if 'book_id' in request_keys and request.POST['new_state'] in ('Completado', 'En proceso', 'Abandonado', 'En espera'):
            book_id = request.POST['book_id']
            book = BookList.objects.get(user_id=user.id, book_id=book_id)

            book.state = request.POST['new_state']
            book.save()
            user.save()
            toast_title = f"'{Book.objects.get(id=book_id).title}' ha sido editado con éxito."

        elif 'delete_id' in request_keys:
            book_id = request.POST['delete_id']
            book = Book.objects.get(id=book_id)
            user.books.remove(book)
            user.save()
            toast_title = f"'{book.title}' ha sido eliminado con éxito."
        
        elif 'new_book_id' in request_keys and request.POST['state'] in ('Completado', 'En proceso', 'Abandonado', 'En espera'):
            book = Book.objects.get(id=request.POST['new_book_id'])
            user.books.add(book)
            book_in_user_booklist = BookList.objects.get(user_id=user.id, book_id=book.id)
            book_in_user_booklist.state = request.POST['state']
            book_in_user_booklist.save()
            user.save()
            toast_title = f"'{book.title}' ha sido añadido con éxito."

        if toast_title:
            toast = '''Swal.mixin({{
                        title: "{title}",
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
                    }})'''.format_map({'title': toast_title, })

        if 'order_by' in request_keys:
            column = request.POST['order_by']
            if column == 'id':
                user_booklist = BookList.objects.filter(user_id=request.user.id, state=STATES[state][0])
            else:
                user_booklist = BookList.objects.filter(user_id=request.user.id, state=STATES[state][0]).order_by(f"book__{column}")

    if not user_booklist:
        user_booklist = BookList.objects.filter(user_id=request.user.id, state=STATES[state][0])

    books = [Book.objects.get(id=book.book_id) for book in user_booklist]

    books_not_in_user = BookList.objects.filter(user_id=request.user.id).values_list('book_id', flat=True)
    queryset_books_to_add = Book.objects.exclude(id__in=books_not_in_user)
    books_to_add = {}

    for book in queryset_books_to_add:
        books_to_add[book.id] = book.title

    context = {
        'state': STATES[state][0],
        'title': STATES[state][1],
        'books': books,
        'books_to_add': books_to_add,
        'toast': toast
    }

    return render(request, 'detail_list.html', context)

def _get_books_states_count_as_json(user):
    STATES = {
             'Completados': 'Completado', 
             'En proceso': 'En proceso', 
             'Abandonados': 'Abandonado', 
             'En espera': 'En espera'
             }
    statesData = [['Estado', 'Libros'],]

    for state in STATES:
        book_count = BookList.objects.filter(user_id=user.id, state=STATES[state]).count()
        statesData.append([state, book_count])
    
    statesData = json.dumps(statesData)
    return statesData

def _get_authors_count_as_json(user):
    STATES = {
             'Completados': 'Completado', 
             'En proceso': 'En proceso', 
             'Abandonados': 'Abandonado', 
             'En espera': 'En espera'
             }
    authorsData = [['Autores', 'Completados', 'En proceso', 'Abandonados', 'En espera'],]

    booklist_authors_queryset = BookList.objects.filter(user_id=user.id).values_list('book_id__author', flat=True)
    distinct_booklist_authors = list(set(booklist_authors_queryset))

    for author in distinct_booklist_authors:
        author_count = [author, ]
        for state in STATES:
            author_state_count = BookList.objects\
                                                .filter(
                                                        user_id=user.id, 
                                                        book_id__author=author, 
                                                        state=STATES[state]
                                                        )\
                                                .count()
            author_count.append(author_state_count)
        
        authorsData.append(author_count)
    
    authorsData = json.dumps(authorsData)
    return authorsData

def _get_genres_count_as_json(user):
    GENRES = {
        'Acción': 'Acción',
        'Novela': 'Novela',
        'Aventuras': 'Aventuras',
        'Ciencia Ficcion': 'Ciencia Ficción',
        'Tragedia': 'Tragedia',
        'Fantasía': 'Fantasía',
        'Documental': 'Documental',
        'Drama': 'Drama',
        'Musical': 'Musical',
        'Comedia': 'Comedia',
        'Suspense': 'Suspense',
        'Terror': 'Terror',
        'Juvenil': 'Juvenil',
        'Romance': 'Romance',
        'Autobiografía': 'Autobiografía',
    }

    genres_data = [['Género', 'Libros'],]
    for genre in GENRES:
        genre_book_count = BookList.objects.filter(user_id = user.id, book_id__genre=genre).count()
        genres_data.append([genre, genre_book_count])

    genres_data = json.dumps(genres_data)
    return genres_data
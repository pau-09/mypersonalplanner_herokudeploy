import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Book
from users.models import BookList


@login_required(login_url="login")
def booksView(request):
    """
    Books general view.
    Will display 3 grafics:
        1. Count of books on each list states.
        2. Count of distinct authors added on each state lists.
        3. Count of each book genres added.
    """

    statesData = _get_books_states_count_as_json(request.user)
    authorsData = _get_authors_count_as_json(request.user)
    genresData = _get_genres_count_as_json(request.user)
    total_count = BookList.objects.filter(user_id=request.user.id).count()

    context = {
        "entry_type": "libros",
        "statesData": statesData,
        "authorsData": authorsData,
        "genresData": genresData,
        "total_count": total_count,
    }

    return render(request, "list_summary.html", context)


@login_required(login_url="login")
def bookListDetailView(request, state):
    """
    Books list detail view.
    Will display a table of books added in list of given state,
    each row displays a book and will include
    adding, editing and deleting functionalities.
    """

    STATES = {
        "completos": ["Completado", "completados"],
        "en-proceso": ["En proceso", "en proceso"],
        "abandonados": ["Abandonado", "abandonados"],
        "en-espera": ["En espera", "en lista de espera"],
    }
    current_state = STATES[state][0]
    title = f"Libros {STATES[state][1]}"
    toast_title = ""
    user_booklist = list()
    user = request.user

    if request.method == "POST":
        request_keys = request.POST.keys()

        if "book_id" in request_keys and "new_state" in request_keys:
            book_id = request.POST["book_id"]
            new_state = request.POST["new_state"]
            toast_title = _update_book_state(user, book_id, new_state)

        elif "delete_id" in request_keys:
            book_id = request.POST["delete_id"]
            toast_title = _delete_book_from_list(user, book_id)

        elif "new_book_id" in request_keys and "state" in request_keys:
            book_id = request.POST["new_book_id"]
            state = request.POST["state"]
            toast_title = _add_book_to_list(user, book_id, state)

        user_booklist = BookList.objects.filter(
            user_id=user.id, state=current_state
        )

        if "order_by" in request_keys:
            column = request.POST["order_by"]
            if column != "id":
                user_booklist = user_booklist.order_by(f"book__{column}")

    if not user_booklist:
        user_booklist = BookList.objects.filter(
            user_id=user.id, state=current_state
        )

    books = [Book.objects.get(id=book.book_id) for book in user_booklist]
    books_not_in_user = BookList.objects.filter(user_id=user.id).values_list(
        "book_id", flat=True
    )
    queryset_books_to_add = Book.objects.exclude(id__in=books_not_in_user)
    books_to_add = dict()

    for book in queryset_books_to_add:
        books_to_add[book.id] = book.title

    context = {
        "state": current_state,
        "title": title,
        "books": books,
        "books_to_add": books_to_add,
        "toast_title": toast_title,
    }

    return render(request, "detail_list.html", context)


def _update_book_state(user, book_id, new_state):
    """
    Updates the state of a booklist object given:
        1. User.
        2. Book object id.
        3. New state.

    Checks new state and returns success toast title as string if it's valid,
    doesn't do nothig if it's invalid.
    """
    state_options = ("Completado", "En proceso", "Abandonado", "En espera")

    if new_state in state_options:

        book = Book.objects.get(id=book_id)

        booklist_object = BookList.objects.get(user_id=user.id, book_id=book_id)
        booklist_object.state = new_state
        booklist_object.save()
        user.save()

        return f"'{book.title}' ha sido editado con éxito."


def _delete_book_from_list(user, book_id):
    """
    Deletes book as booklist object given:
        1. User.
        2. Book object id.

    Returns success toast title as string
    """
    book = Book.objects.get(id=book_id)
    user.books.remove(book)
    user.save()

    return f"'{book.title}' ha sido eliminado con éxito."


def _add_book_to_list(user, book_id, state):
    """
    Adds booklist object given:
        1. User.
        2. Book object id.
        3. State.

    Checks new state and returns success toast title as string if it's valid,
    doesn't do nothig if it's invalid.
    """

    state_options = ("Completado", "En proceso", "Abandonado", "En espera")

    if state in state_options:
        book = Book.objects.get(id=book_id)
        user.books.add(book)
        book_in_user_booklist = BookList.objects.get(
            user_id=user.id, book_id=book.id
        )
        book_in_user_booklist.state = state
        book_in_user_booklist.save()
        user.save()
        return f"'{book.title}' ha sido añadido con éxito."


def _get_books_states_count_as_json(user):
    """
    Gets the count of books for each state given the user.
    Returns it as json.
    """

    STATES = {
        "Completados": "Completado",
        "En proceso": "En proceso",
        "Abandonados": "Abandonado",
        "En espera": "En espera",
    }
    statesData = [
        ["Estado", "Libros"],
    ]

    for state in STATES:
        book_count = BookList.objects.filter(
            user_id=user.id, state=STATES[state]
        ).count()
        statesData.append([state, book_count])

    statesData = json.dumps(statesData)
    return statesData


def _get_authors_count_as_json(user):
    """
    Gets the count of books for each author given the user.
    Returns it as json.
    """

    STATES = {
        "Completados": "Completado",
        "En proceso": "En proceso",
        "Abandonados": "Abandonado",
        "En espera": "En espera",
    }
    authorsData = [
        ["Autores", "Completados", "En proceso", "Abandonados", "En espera"],
    ]

    booklist_authors_queryset = BookList.objects.filter(
        user_id=user.id
    ).values_list("book_id__author", flat=True)
    distinct_booklist_authors = list(set(booklist_authors_queryset))

    for author in distinct_booklist_authors:
        author_count = [
            author,
        ]
        for state in STATES:
            author_state_count = BookList.objects.filter(
                user_id=user.id, book_id__author=author, state=STATES[state]
            ).count()
            author_count.append(author_state_count)

        authorsData.append(author_count)

    authorsData = json.dumps(authorsData)
    return authorsData


def _get_genres_count_as_json(user):
    GENRES = {
        "Acción": "Acción",
        "Novela": "Novela",
        "Aventuras": "Aventuras",
        "Ciencia Ficcion": "Ciencia Ficción",
        "Tragedia": "Tragedia",
        "Fantasía": "Fantasía",
        "Documental": "Documental",
        "Drama": "Drama",
        "Musical": "Musical",
        "Comedia": "Comedia",
        "Suspense": "Suspense",
        "Terror": "Terror",
        "Juvenil": "Juvenil",
        "Romance": "Romance",
        "Autobiografía": "Autobiografía",
    }

    genres_data = [
        ["Género", "Libros"],
    ]

    for genre in GENRES:
        genre_book_count = BookList.objects.filter(
            user_id=user.id, book_id__genre=genre
        ).count()
        genres_data.append([genre, genre_book_count])

    genres_data = json.dumps(genres_data)
    return genres_data
